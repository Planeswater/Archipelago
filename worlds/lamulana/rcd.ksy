meta:
  id: rcd
  file-extension: rcd
  endian: be
seq:
  - id: unknown
    type: s2
  - id: zones
    type: zone(_index)
    repeat: expr
    repeat-expr: 26
  - id: padding
    type: str
    encoding: UTF-8
    size-eos: true
types:
  operation:
    seq:
      - id: flag
        type: s2
      - id: op_value
        type: s1
      - id: operation
        type: s1
  object_with_position:
    seq:
      - id: id
        type: s2
      - id: test_operations_length
        type: b4
      - id: write_operations_length
        type: b4
      - id: parameters_length
        type: s1
      - id: x_pos
        type: s2
      - id: y_pos
        type: s2
      - id: test_operations
        type: operation
        repeat: expr
        repeat-expr: test_operations_length
      - id: write_operations
        type: operation
        repeat: expr
        repeat-expr: write_operations_length
      - id: parameters
        type: s2
        repeat: expr
        repeat-expr: parameters_length
  object_without_position:
    seq:
      - id: id
        type: s2
      - id: test_operations_length
        type: b4
      - id: write_operations_length
        type: b4
      - id: parameters_length
        type: s1
      - id: test_operations
        type: operation
        repeat: expr
        repeat-expr: test_operations_length
      - id: write_operations
        type: operation
        repeat: expr
        repeat-expr: write_operations_length
      - id: parameters
        type: s2
        repeat: expr
        repeat-expr: parameters_length
  exit:
    seq:
      - id: field_id
        type: s1
      - id: room_id
        type: s1
      - id: screen_id
        type: s1
  screen:
    seq:
      - id: screen_name_length
        type: s1
      - id: objects_length
        type: s2
      - id: objects_without_position_length
        type: s1
      - id: objects_without_position
        type: object_without_position
        repeat: expr
        repeat-expr: objects_without_position_length
      - id: objects_with_position
        type: object_with_position
        repeat: expr
        repeat-expr: objects_length - objects_without_position_length
      - id: screen_name
        type: s1
        repeat: expr
        repeat-expr: screen_name_length
      - id: exits
        type: exit
        repeat: expr
        repeat-expr: 4
  room:
    params:
      - id: zone_index
        type: u1
      - id: room_index
        type: u1
    seq:
      - id: objects_length
        type: s2
      - id: objects
        type: object_without_position
        repeat: expr
        repeat-expr: objects_length
      - id: screens
        type: screen
        repeat: expr
        repeat-expr: _root.zone_sizes[zone_index][room_index]
  zone:
    params:
      - id: zone_index
        type: u1
    seq:
      - id: zone_name_length
        type: s1
      - id: objects_length
        type: s2
      - id: zone_name
        type: s1
        repeat: expr
        repeat-expr: zone_name_length
      - id: objects
        type: object_without_position
        repeat: expr
        repeat-expr: objects_length
      - id: rooms
        type: room(zone_index, _index)
        repeat: expr
        repeat-expr: _root.zone_sizes[zone_index].size
instances:
  zone_sizes:
    value: '[[2,2,2,2,3,1,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,2,2,1,3,3,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,1,1,3,2,3,3,1,0,0,0,0,0,0,0,0,0,0],[2,3,2,1,6,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,1,2,5,1,2,2,2,2,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],[2,2,3,3,1,2,1,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,3,3,2,2,2,2,2,2,2,3,3,2,2,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,4,4,4,4,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,3,1,2,2,1,3,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,2,2,1,4,2,1,2,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,1,4,2,2,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,3,2,2,2,4,3,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],[3,2,2,2,2,2,2,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,3,0,0,0,0,0,0,0,0],[2,2,2,1,2,2,1,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,2,2,2,2,2,2,2,2,2,0,0,0,0,0],[2,3,2,2,2],[2,3,2,2,2],[2,0],[3,2,2,1,3,3,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0],[1,2,2,1,2,2,2,1,2,2,2,1,2,1,2,2,1,1,2,1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,1,2,0,0],[5,5,5,5,0]]'

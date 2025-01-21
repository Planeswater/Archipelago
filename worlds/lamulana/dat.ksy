meta:
  id: dat
  file-extension: dat
  endian: be
seq:
  - id: num_cards
    type: u2
  - id: cards
    type: card
    repeat: expr
    repeat-expr: num_cards
types:
  card:
    seq:
      - id: len_contents
        type: u2
      - id: contents
        type: card_contents
        size: len_contents
  card_contents:
    seq:
      - id: entries
        type: entry
        repeat: eos
  entry:
    seq:
      - id: header
        type: u2
        enum: entry_header
      - id: contents
        type:
          switch-on: header
          cases:
            'entry_header::flag': flag
            'entry_header::flag2': flag2
            'entry_header::item': item
            'entry_header::pose': pose
            'entry_header::mantra': mantra
            'entry_header::color': color
            'entry_header::item_name': item_name
            'entry_header::data': data
            'entry_header::anime': anime
            _: noop
  flag:
    seq:
      - id: address
        type: s2
      - id: value
        type: s2
  flag2:
    seq:
      - id: address
        type: s2
      - id: value
        type: s2
  item:
    seq:
      - id: value
        type: s2
  pose:
    seq:
      - id: value
        type: s2
  mantra:
    seq:
      - id: value
        type: s2
  color:
    seq:
      - id: red
        type: s2
      - id: green
        type: s2
      - id: blue
        type: s2
  item_name:
    seq:
      - id: value
        type: s2
  data:
    seq:
      - id: num_values
        type: s2
      - id: values
        type: s2
        repeat: expr
        repeat-expr: num_values
  anime:
    seq:
      - id: value
        type: s2
  noop:
    seq:
      - id: no_value
        size: 0
enums:
  entry_header:
    0x0040: flag
    0x0041: flag2
    0x0042: item
    0x0046: pose
    0x0047: mantra
    0x004a: color
    0x004d: item_name
    0x004e: data
    0x004f: anime

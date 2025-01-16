meta:
  id: sav
  file-extension: sav
  endian: be
seq:
  - id: valid
    type: u1
  - id: game_time
    type: u4
  - id: zone
    type: u1
  - id: room
    type: u1
  - id: screen
    type: u1
  - id: x_position
    type: u2
  - id: y_position
    type: u2
  - id: max_hp
    type: u1
  - id: current_hp
    type: u2
  - id: current_exp
    type: u2
  - id: flags
    type: u1
    repeat: expr
    repeat-expr: 4096
  - id: inventory
    type: u2
    repeat: expr
    repeat-expr: 255
  - id: held_main_weapon
    type: u1
  - id: held_sub_weapon
    type: u1
  - id: held_use_item
    type: u1
  - id: held_main_weapon_slot
    type: u1
  - id: held_sub_weapon_slot
    type: u1
  - id: held_use_item_slot
    type: u1
  - id: num_emails
    type: u2
  - id: received_emails
    type: u2
  - id: emails
    type: email
    repeat: expr
    repeat-expr: num_emails
  - id: equipped_software
    type: u1
    repeat: expr
    repeat-expr: 20
  - id: rosettas_read
    type: u2
    repeat: expr
    repeat-expr: 3
  - id: bunemon_records
    type: bunemon_record
    repeat: expr
    repeat-expr: 20
  - id: mantras_learned
    type: u1
    repeat: expr
    repeat-expr: 10
  - id: maps_owned_bit_array
    type: u4
types:
  email:
    seq:
      - id: screenplay_card
        type: u2
      - id: game_time_received
        type: u4
      - id: mail_number
        type: u2
  bunemon_record:
    seq:
      - id: slot_number
        type: u1
      - id: field_map_card
        type: u2
      - id: field_map_record
        type: u2
      - id: location_card
        type: u2
      - id: location_record
        type: u2
      - id: text_card
        type: u2
      - id: text_record
        type: u2
      - id: is_tablet
        type: u1

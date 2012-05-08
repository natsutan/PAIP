# -*- coding: utf-8 -*-
import gps2

banana_ops = [
    gps2.operator('clime-on-chiar', 
                  ('chair-at-middle-room', 'at-middle-room', 'on-floor'),
                  ('at-bananas', 'on-char'),
                  ('at-middle-room', 'on-floor')),
    gps2.operator('push-chair-from-door-to-middle-room',
                  ('chair-at-door', 'at-door'),
                  ('chair-at-middle-room', 'at-middle-room'),
                  ('chair-at-door', 'at-door')),
    gps2.operator('walk-from-door-to-middle-room',
                  ('at-door', 'on-floor'),
                  ('at-middle-room',),
                  ('at-door',)),
    gps2.operator('grasp-bananas',
                  ('at-bananas', 'empty-handed'),
                  ('has-bananas',),
                  ('empty-handed',)),
    gps2.operator('drop-ball',
                  ('has-ball',),
                  ('empty-handed',),
                  ('has-ball',)),
    gps2.operator('eat-bananas',
                  ('has-bananas',),
                  ('empty-handed', 'not-hungry'),
                  ('has-bananas', 'hungry'))
    ]
    

gps2.use(banana_ops)
print gps2.gps2( ('at-door', 'on-floor', 'has-ball', 'hungry', 'chair-at-door'),
                 ('not-hungry',),
                 banana_ops)

  

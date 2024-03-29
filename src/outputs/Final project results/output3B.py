# arquitetura: batch de 1024, 5 camadas "relu" 1 camada "softmax", 150 épocas
from fractions import Fraction

output = [[Fraction(0, 1), 'Tempo', '120.0'],
[Fraction(0, 1), 'Formula de Compasso', '4/4'],
[Fraction(0, 1), 'Note', 'Parte_4', Fraction(1, 2), 56, None],
[Fraction(0, 1), 'Tuplet 3:2', 'Parte_1', [['Rest', Fraction(1, 2), 0, None], ['Note', Fraction(1, 2), 52, None], ['Note', Fraction(1, 2), 52, None]]],
[Fraction(0, 1), 'Rest', 'Parte_2', Fraction(4, 1), 0, None],
[Fraction(0, 1), 'Note', 'Parte_3', Fraction(4, 1), 44, None],
[Fraction(1, 2), 'Note', 'Parte_4', Fraction(4, 1), 44, None],
[Fraction(0, 1), 'Rest', 'Parte_6', Fraction(4, 1), 0, None],
[Fraction(4, 1), 'Rest', 'Parte_6', Fraction(4, 1), 0, None],
[Fraction(8, 1), 'Rest', 'Parte_6', Fraction(4, 1), 0, None],
[Fraction(8, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 54, None], ['Note', Fraction(1, 2), 54, None], ['Note', Fraction(1, 2), 54, None]]],
[Fraction(9, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 54, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(10, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(11, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(12, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(13, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(14, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(15, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(16, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(17, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(18, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(19, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(20, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(21, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(22, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(23, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(24, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(25, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(26, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(27, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(28, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(29, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(30, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(31, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(32, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(33, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(34, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(35, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(36, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]],
[Fraction(37, 1), 'Tuplet 3:2', 'Parte_3', [['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None], ['Note', Fraction(1, 2), 59, None]]]]
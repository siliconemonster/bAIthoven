# arquitetura: batch de 1024, 3 camadas "relu" 1 camada "softmax", 250 épocas
from fractions import Fraction

output = [[Fraction(0, 1), 'Tempo', '120.0'],
[Fraction(0, 1), 'Formula de Compasso', '4/4'],
[Fraction(0, 1), 'Note', 'Parte_3', Fraction(1, 1), 50, None],
[Fraction(0, 1), 'Note', 'Parte_1', Fraction(1, 1), 67, None],
[Fraction(0, 1), 'Note', 'Parte_2', Fraction(1, 1), 60, None],
[Fraction(0, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(1, 1), 'Note', 'Parte_1', Fraction(1, 1), 60, None],
[Fraction(1, 1), 'Note', 'Parte_3', Fraction(1, 1), 60, None],
[Fraction(1, 1), 'Rest', 'Parte_4', Fraction(1, 1), 0, None],
[Fraction(2, 1), 'Note', 'Parte_4', Fraction(1, 1), 60, None],
[Fraction(3, 1), 'Note', 'Parte_4', Fraction(1, 1), 60, None],
[Fraction(0, 1), 'Note', 'Parte_5', Fraction(1, 1), 54, None],
[Fraction(1, 1), 'Rest', 'Parte_5', Fraction(4, 1), 0, None],
[Fraction(0, 1), 'Rest', 'Parte_6', Fraction(4, 1), 0, None],
[Fraction(2, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(4, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(5, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(6, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(4, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(5, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(4, 1), 'Note', 'Parte_3', Fraction(1, 1), 50, None],
[Fraction(6, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(7, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(4, 1), 'Note', 'Parte_2', Fraction(1, 1), 67, None],
[Fraction(5, 1), 'Note', 'Parte_2', Fraction(1, 1), 50, None],
[Fraction(7, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(8, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(9, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(10, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(11, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(12, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(12, 1), 'Note', 'Parte_5', Fraction(1, 1), 54, None],
[Fraction(12, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(13, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(13, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(14, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(15, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(14, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(15, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(12, 1), 'Note', 'Parte_3', Fraction(1, 1), 50, None],
[Fraction(16, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(17, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(16, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(16, 1), 'Note', 'Parte_2', Fraction(1, 1), 50, None],
[Fraction(18, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(19, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(17, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(20, 1), 'Chord', 'Parte_4', Fraction(1, 1), [50, 54], None],
[Fraction(21, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(22, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(23, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(20, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(24, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(24, 1), 'Note', 'Parte_1', Fraction(1, 1), 67, None],
[Fraction(25, 1), 'Note', 'Parte_1', Fraction(1, 1), 67, None],
[Fraction(24, 1), 'Note', 'Parte_2', Fraction(1, 1), 50, None],
[Fraction(25, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(26, 1), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(27, 1), 'Note', 'Parte_1', Fraction(1, 1), 67, None],
[Fraction(26, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(27, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(28, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(29, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(30, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(31, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(32, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(33, 1), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(34, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(35, 1), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(36, 1), 'Rest', 'Parte_4', Fraction(4, 1), 0, None],
[Fraction(36, 1), 'Note', 'Parte_1', Fraction(1, 2), 63, None],
[Fraction(40, 1), 'Note', 'Parte_4', Fraction(1, 2), 63, None],
[Fraction(81, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(40, 1), 'Note', 'Parte_1', Fraction(1, 1), 73, None],
[Fraction(41, 1), 'Note', 'Parte_1', Fraction(1, 1), 76, None],
[Fraction(40, 1), 'Rest', 'Parte_2', Fraction(1, 1), 0, None],
[Fraction(83, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(85, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(87, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(89, 2), 'Rest', 'Parte_4', Fraction(1, 1), 0, None],
[Fraction(91, 2), 'Rest', 'Parte_4', Fraction(1, 1), 0, None],
[Fraction(93, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(89, 2), 'Note', 'Parte_1', Fraction(1, 1), 60, None],
[Fraction(95, 2), 'Note', 'Parte_4', Fraction(1, 1), 60, None],
[Fraction(97, 2), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(99, 2), 'Note', 'Parte_4', Fraction(1, 1), 54, None],
[Fraction(101, 2), 'Rest', 'Parte_4', Fraction(4, 1), 0, None],
[Fraction(97, 2), 'Rest', 'Parte_5', Fraction(4, 1), 0, None],
[Fraction(105, 2), 'Rest', 'Parte_5', Fraction(4, 1), 0, None],
[Fraction(113, 2), 'Rest', 'Parte_5', Fraction(4, 1), 0, None],
[Fraction(113, 2), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(113, 2), 'Note', 'Parte_3', Fraction(1, 1), 50, None],
[Fraction(113, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(115, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(115, 2), 'Note', 'Parte_1', Fraction(1, 1), 50, None],
[Fraction(117, 2), 'Note', 'Parte_1', Fraction(1, 1), 67, None],
[Fraction(113, 2), 'Note', 'Parte_2', Fraction(1, 1), 50, None],
[Fraction(117, 2), 'Note', 'Parte_4', Fraction(1, 1), 50, None],
[Fraction(119, 2), 'Note', 'Parte_1', Fraction(1, 1), 60, None]]
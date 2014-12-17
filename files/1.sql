SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM `settings`;

ALTER TABLE `settings` AUTO_INCREMENT = 0;

INSERT INTO `settings` (`id`, `key`, `value`) VALUES
    (1, 'username', 'parryj90'),
    (2, 'password', '$2a$10$QPmQHY3tusaZH2GD6rTtaOE68qNaz9Ilco03R93Fj/KzyydmDZYPe');

DELETE FROM `categories`;

ALTER TABLE `categories` AUTO_INCREMENT = 0;

INSERT INTO `categories` (`id`, `name`, `position`) VALUES
    (1, 'Music', 1),
    (2, 'Food & Beverage', 2),
    (4, 'Sports', 3),
    (5, 'Food Trucks', 4),
    (6, 'Happy Hours', 5),
    (7, 'Trivia', 6),
    (8, 'Community', 7);

DELETE FROM `handles`;

ALTER TABLE `handles` AUTO_INCREMENT = 0;

INSERT INTO `handles` (`id`, `name`, `summary`) VALUES
    (1, 'mercylounge', 'The Mercy Lounge nashville Music King'),
    (2, 'BrdgstoneArena', 'Bridgestone Arena'),
    (3, 'tavernnashville', 'Tavern Nashville'),
    (5, 'GrlldCheeserie', 'The Grilled Cheeserie'),
    (16, 'NashFoodTrucks', 'Your one stop for Nashville food trucks! Check back for daily locations & updates!'),
    (18, 'NashvilleTrivia', 'Challenge Entertainment brings Live Team Trivia to the Nashville area. Bring a Team and Win Some Green!!!'),
    (19, 'TheBasementNash', 'Enter a brief summary of the handle...'),
    (20, '3rdandLindsley', 'Enter a brief summary of the handle...'),
    (21, '12th_and_Porter', 'Enter a brief summary of the handle...'),
    (22, 'canneryballroom', 'Enter a brief summary of the handle...'),
    (23, 'thehighwatt', 'Enter a brief summary of the handle...'),
    (24, 'FidoNashville', 'Enter a brief summary of the handle...'),
    (25, 'SamsSportsGrill', 'Enter a brief summary of the handle...'),
    (26, 'nashvillesounds', 'Enter a brief summary of the handle...'),
    (27, 'PredsNHL', 'Enter a brief summary of the handle...'),
    (28, 'TennesseeTitans', 'Enter a brief summary of the handle...'),
    (29, 'VandyMBB', 'Enter a brief summary of the handle...'),
    (30, 'VandyFootball', 'Enter a brief summary of the handle...'),
    (31, 'BelmontMBB', 'Enter a brief summary of the handle...'),
    (32, 'DoughworksTruck', 'Enter a brief summary of the handle...'),
    (33, 'PM_Nashville', 'Enter a brief summary of the handle...'),
    (34, 'TinRoofNash', 'Enter a brief summary of the handle...'),
    (35, 'SouthNashville', 'Enter a brief summary of the handle...'),
    (36, 'SlowHandCoffee', 'Enter a brief summary of the handle...'),
    (37, 'BaconNationNash', 'Enter a brief summary of the handle...'),
    (38, 'SmokeEtAl', 'Enter a brief summary of the handle...'),
    (39, 'crepeadiem', 'Enter a brief summary of the handle...'),
    (40, 'RetroSno', 'Enter a brief summary of the handle...'),
    (41, 'crankees', 'Enter a brief summary of the handle...'),
    (43, 'ClimbNashville', 'Enter a brief summary of the handle...'),
    (44, 'NashvilleZoo', 'Enter a brief summary of the handle...'),
    (47, '12SouthNash', 'Enter a brief summary of the handle...'),
    (48, '12southtaproom', 'Enter a brief summary of the handle...'),
    (51, 'MAFIAoZAS_Nash', 'Enter a brief summary of the handle...'),
    (54, 'ThePharmacy1', 'Enter a brief summary of the handle...'),
    (57, 'mastacos', 'Enter a brief summary of the handle...'),
    (58, 'JacksonsNash', 'Enter a brief summary of the handle...'),
    (60, 'GreenhouseBar', 'Enter a brief summary of the handle...'),
    (63, 'pub5nash', 'Enter a brief summary of the handle...'),
    (66, 'Exit_In', 'Enter a brief summary of the handle...'),
    (67, 'BluebirdCafeTN', 'Enter a brief summary of the handle...'),
    (68, 'SylvanPark615', 'Enter a brief summary of the handle...'),
    (69, 'McCabePub', 'Enter a brief summary of the handle...'),
    (72, 'RippysNashville', 'Enter a brief summary of the handle...'),
    (78, 'error', 'Error');

DELETE FROM `categories_handles`;

ALTER TABLE `categories_handles` AUTO_INCREMENT = 0;

INSERT INTO `categories_handles` (`id`, `category_id`, `handle_id`) VALUES
    (1, 1, 1),
    (2, 1, 2),
    (3, 2, 3),
    (5, 5, 16),
    (6, 7, 18),
    (7, 1, 19),
    (8, 1, 20),
    (9, 1, 21),
    (10, 1, 22),
    (11, 1, 23),
    (12, 2, 24),
    (13, 2, 25),
    (14, 4, 26),
    (15, 4, 27),
    (16, 4, 28),
    (17, 4, 29),
    (18, 4, 30),
    (19, 4, 31),
    (20, 5, 32),
    (21, 2, 33),
    (22, 2, 34),
    (23, 2, 35),
    (24, 5, 36),
    (25, 5, 37),
    (26, 5, 38),
    (27, 5, 39),
    (28, 5, 40),
    (29, 5, 41),
    (30, 8, 43),
    (31, 8, 44),
    (34, 8, 47),
    (35, 2, 48),
    (38, 2, 51),
    (41, 2, 54),
    (44, 2, 57),
    (45, 2, 58),
    (47, 2, 60),
    (50, 2, 63),
    (53, 1, 66),
    (54, 1, 67),
    (55, 8, 68),
    (56, 2, 69),
    (59, 2, 72),
    (93, 5, 5),
    (99, 8, 78),
    (100, 6, 69),
    (101, 7, 69),
    (102, 6, 63),
    (103, 7, 63),
    (104, 6, 60),
    (105, 7, 60),
    (106, 6, 58),
    (107, 6, 54),
    (108, 7, 54),
    (109, 6, 51),
    (110, 7, 51),
    (111, 6, 48),
    (112, 7, 48),
    (113, 6, 25),
    (114, 7, 25);

SET FOREIGN_KEY_CHECKS = 1;

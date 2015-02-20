DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) COLLATE utf8_unicode_ci,
    `password` VARCHAR(255) COLLATE utf8_unicode_ci,
    `twitter_screen_name` VARCHAR(255) COLLATE utf8_unicode_ci,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    UNIQUE KEY `twitter_screen_name` (`twitter_screen_name`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

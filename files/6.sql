DROP TABLE IF EXISTS `tweets`;
CREATE TABLE IF NOT EXISTS `tweets` (
    `id` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `user_name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `user_profile_image_url` VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `user_screen_name` VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `created_at` DATETIME NOT NULL,
    `favorites` INT(11) UNSIGNED NOT NULL,
    `media` TEXT COLLATE utf8_unicode_ci NOT NULL,
    `retweets` INT(11) UNSIGNED NOT NULL,
    `text` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    KEY `created_at` (`created_at`),
    KEY `user_screen_name` (`user_screen_name`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

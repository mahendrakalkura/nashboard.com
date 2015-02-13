DROP TABLE IF EXISTS `social_users`;
CREATE TABLE IF NOT EXISTS `social_users` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `password` VARCHAR(255) COLLATE utf8_unicode_ci,
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_name` (`user_name`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

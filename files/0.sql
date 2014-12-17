SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `settings`;
CREATE TABLE IF NOT EXISTS `settings` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `key` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `value` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `key` (`key`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `position` INT(11) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `position` (`position`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `handles`;
CREATE TABLE IF NOT EXISTS `handles` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `profile_image_url` VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `screen_name` VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    `summary` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `profile_image_url` (`profile_image_url`),
    KEY `screen_name` (`screen_name`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `categories_handles`;
CREATE TABLE IF NOT EXISTS `categories_handles` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `category_id` INT(11) UNSIGNED NOT NULL,
    `handle_id` INT(11) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `category_id_handle_id` (`category_id`, `handle_id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

DROP TABLE IF EXISTS `tweets`;
CREATE TABLE IF NOT EXISTS `tweets` (
    `id` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `handle_id` INT(11) UNSIGNED NOT NULL,
    `created_at` DATETIME NOT NULL,
    `media` TEXT COLLATE utf8_unicode_ci NOT NULL,
    `text` TEXT COLLATE utf8_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    KEY `created_at` (`created_at`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

ALTER TABLE `categories_handles`
    ADD CONSTRAINT `categories_handles_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `categories` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `categories_handles`
    ADD CONSTRAINT `categories_handles_handle_id`
    FOREIGN KEY (`handle_id`)
    REFERENCES `handles` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `tweets`
    ADD CONSTRAINT `tweets_handle_id`
    FOREIGN KEY (`handle_id`)
    REFERENCES `handles` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

SET FOREIGN_KEY_CHECKS = 1;

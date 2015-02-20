DROP TABLE IF EXISTS `votes`;
CREATE TABLE IF NOT EXISTS `votes` (
    `id` INT(11) COLLATE utf8_unicode_ci NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) UNSIGNED NOT NULL,
    `tweet_id` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `direction` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
    `timestamp` DATETIME NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `user_id_tweet_id` (`user_id`, `tweet_id`),
    KEY `direction` (`direction`),
    KEY `timestamp` (`timestamp`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

ALTER TABLE `votes`
    ADD CONSTRAINT `votes_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `votes`
    ADD CONSTRAINT `votes_tweet_id`
    FOREIGN KEY (`tweet_id`)
    REFERENCES `tweets` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

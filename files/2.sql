ALTER TABLE `categories`
    ADD `ttl` INT(11) UNSIGNED NOT NULL DEFAULT 604800 AFTER `name`;

ALTER TABLE `categories` ADD INDEX `ttl` (`ttl`) ;

SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE `tweets` ADD `favorites` INT NOT NULL AFTER `created_at`;
ALTER TABLE `tweets` ADD INDEX (`favorites`) ;

ALTER TABLE `tweets` ADD `retweets` INT NOT NULL AFTER `media`;
ALTER TABLE `tweets` ADD INDEX (`retweets`) ;

SET FOREIGN_KEY_CHECKS = 1;

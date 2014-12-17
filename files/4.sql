DROP TABLE IF EXISTS `neighborhoods`;
CREATE TABLE IF NOT EXISTS `neighborhoods` (
    `id` INTEGER(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `position`  INTEGER(11) UNSIGNED NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `name` (`name`),
    KEY `position` (`position`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=0;

INSERT INTO `neighborhoods` (`id`, `name`, `position`) VALUES
    (1, 'Neighborhood #1', '1');

ALTER TABLE `handles`
    ADD `neighborhood_id` INT(11) UNSIGNED NOT NULL AFTER `id`;

UPDATE `handles` SET `neighborhood_id` = 1;

ALTER TABLE `handles` ADD INDEX `neighborhood_id` (`neighborhood_id`) ;

ALTER TABLE `handles`
    ADD CONSTRAINT `handles_neighborhood_id`
    FOREIGN KEY (`neighborhood_id`)
    REFERENCES `neighborhoods` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

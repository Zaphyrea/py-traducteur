-- Adminer 4.8.1 MySQL 8.2.0 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS `prompts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text_in` varchar(250) NOT NULL,
  `text_out` varchar(250) NOT NULL,
  `version` varchar(250) NOT NULL,
  `utilisateur` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `utilisateur` (`utilisateur`),
  CONSTRAINT `prompts_ibfk_1` FOREIGN KEY (`utilisateur`) REFERENCES `utilisateurs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `prompts` (`id`, `text_in`, `text_out`, `version`, `utilisateur`) VALUES
(1,	'Premièrement, tu ôteras la Goupille sacrée. Puis tu compteras jusqu\'à trois, pas plus, pas moins.',	'First, you\'ll remove the sacred Gull, then you\'ll count to three, no more, no less.',	'fr >> en',	1),
(2,	'Chevaliers qui dites ni, nous ne sommes que de simples voyageurs qui recherchons un enchanteur qui vit au-delà de ces bois.',	'Knights who say neither, we are merely travelers who seek an enchanter who lives beyond these woods.',	'fr >> en',	1);

CREATE TABLE IF NOT EXISTS `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(250) NOT NULL,
  `mdp` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `utilisateurs` (`id`, `login`, `mdp`) VALUES
(1,	'Cleese',	'Sacré Graal!'),
(2,	'Gilliam',	'Flying Circus');

-- 2024-07-10 12:39:49

CREATE TABLE IF NOT EXISTS `latences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `latence_ms` int NOT NULL,
  `version` varchar(250) NOT NULL,
  `statut_code` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `latences_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

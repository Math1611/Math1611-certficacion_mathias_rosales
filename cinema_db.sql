-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema cinepedia_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `cinepedia_db` ;

-- -----------------------------------------------------
-- Schema cinepedia_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cinepedia_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `cinepedia_db` ;

-- -----------------------------------------------------
-- Table `cinepedia_db`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia_db`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `apellido` VARCHAR(100) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `cinepedia_db`.`peliculas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia_db`.`peliculas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  `director` VARCHAR(255) NOT NULL,
  `fecha_estreno` DATE NOT NULL,
  `sinopsis` TEXT NOT NULL,
  `usuario_id` INT NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre` (`nombre` ASC) VISIBLE,
  INDEX `fk_pelis_user` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_pelis_user`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `cinepedia_db`.`usuarios` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `cinepedia_db`.`comentarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cinepedia_db`.`comentarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `contenido` TEXT NOT NULL,
  `usuario_id` INT NOT NULL,
  `pelicula_id` INT NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_com_user` (`usuario_id` ASC) VISIBLE,
  INDEX `fk_com_peli` (`pelicula_id` ASC) VISIBLE,
  CONSTRAINT `fk_com_peli`
    FOREIGN KEY (`pelicula_id`)
    REFERENCES `cinepedia_db`.`peliculas` (`id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_com_user`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `cinepedia_db`.`usuarios` (`id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

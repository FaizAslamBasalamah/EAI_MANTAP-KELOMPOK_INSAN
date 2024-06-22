-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2024 at 07:48 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medis_konsultasi`
--

-- --------------------------------------------------------

--
-- Table structure for table `diseases`
--

CREATE TABLE `diseases` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diseases`
--

INSERT INTO `diseases` (`id`, `name`, `description`) VALUES
(1, 'Kanker', 'Kanker adalah kondisi di mana sel-sel tubuh berkembang secara tidak normal dan tidak terkendali. Ada banyak jenis kanker yang dapat memengaruhi berbagai bagian tubuh, termasuk kanker payudara, kanker paru-paru, kanker prostat, dan lain-lain. Gejala kanker bervariasi tergantung pada jenis dan lokasinya.'),
(2, 'Hiponotia Capilaris', 'Penyakit langka di mana rambut pasien tumbuh memanjang secara ekstrem, melilit tubuh mereka seperti belati berbulu, sering kali membuat mereka sulit untuk bergerak atau melakukan aktivitas sehari-hari. Sementara para peneliti masih mencari penyebab pastinya, beberapa teori menyatakan bahwa ini mungkin terkait dengan perubahan hormonal yang jarang terjadi dalam tubuh manusia.'),
(3, 'Hypertension', 'A condition in which the force of the blood against the artery walls is too high.'),
(4, 'Asthma', 'A condition in which your airways narrow and swell and may produce extra mucus.'),
(5, 'Artritis', 'Artritis adalah kelompok penyakit yang menyebabkan peradangan dan kerusakan pada sendi. Gejalanya meliputi nyeri sendi, kemerahan, pembengkakan, dan kekakuan. Ada beberapa jenis artritis, termasuk osteoartritis, artritis reumatoid, dan lupus.');

-- --------------------------------------------------------

--
-- Table structure for table `konsultasi`
--

CREATE TABLE `konsultasi` (
  `id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `patient_age` int(11) DEFAULT NULL,
  `disease_id` int(11) DEFAULT NULL,
  `nurse_id` int(11) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `management_janji_id` int(11) DEFAULT NULL,
  `resep_hasil_konsultasi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `konsultasi`
--

INSERT INTO `konsultasi` (`id`, `patient_name`, `patient_age`, `disease_id`, `nurse_id`, `patient_id`, `management_janji_id`, `resep_hasil_konsultasi`) VALUES
(26, 'Insan Taufik', 10, 1, 5, 7, NULL, 'Power nap bang'),
(27, 'Jane Smith', 80, 3, 2, 2, NULL, 'Kamu jangan banyak bekerja ini kamu kena kanker'),
(28, 'Insan Taufik', 2000, 4, 5, 7, NULL, 'Kebanyakan ngoding stress jadinya'),
(29, 'Bob Johnson', 1, 1, 2, 4, NULL, 'Kamu hampir keguguran'),
(31, 'Insan Taufik', 29, 5, 2, 7, NULL, 'Jangan lupa shalat'),
(32, 'Insan Taufik', NULL, NULL, 2, 7, 45, NULL),
(33, 'Muhamad Insan Taufik', NULL, NULL, 2, 5190, 46, NULL),
(34, 'Muhamad Insan Taufik', NULL, NULL, 1, 5190, 47, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `management_janji`
--

CREATE TABLE `management_janji` (
  `id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `nurse_name` varchar(100) DEFAULT NULL,
  `appointment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `patient_id` int(11) DEFAULT NULL,
  `nurse_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `management_janji`
--

INSERT INTO `management_janji` (`id`, `patient_name`, `nurse_name`, `appointment_date`, `created_at`, `patient_id`, `nurse_id`) VALUES
(39, 'Insan Taufik', 'Faiz', '2024-06-13 20:06:00', '2024-06-11 20:06:26', 7, 5),
(40, 'Azka Chanda', 'John Doe', '2024-06-13 22:06:00', '2024-06-11 22:06:20', 6, 1),
(41, 'Insan Taufik', 'John Doe', '2024-06-13 22:14:00', '2024-06-11 22:14:11', 7, 1),
(42, 'Bob Johnson', 'Jane Smith', '2024-06-14 22:14:00', '2024-06-11 22:15:02', 4, 2),
(43, 'Insan Taufik', 'John Doe', '2024-06-12 22:51:00', '2024-06-11 22:51:25', 7, 1),
(44, 'Insan Taufik', 'Jane Smith', '2024-06-13 22:40:00', '2024-06-12 22:40:42', 7, 2),
(45, 'Insan Taufik', 'Jane Smith', '2024-06-19 04:32:00', '2024-06-18 04:32:18', 7, 2),
(46, 'Muhamad Insan Taufik', 'Jane Smith', '2024-06-20 04:33:00', '2024-06-18 04:33:54', 5190, 2),
(47, 'Muhamad Insan Taufik', 'John Doe', '2024-06-28 05:24:00', '2024-06-18 05:24:27', 5190, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT 'patient',
  `refresh_token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `password`, `role`, `refresh_token`) VALUES
(1, 'John Doe', 'johndoe', 'doe', 'nurse', NULL),
(2, 'Jane Smith', 'janesmith', 'password5678', 'nurse', NULL),
(4, 'Bob Johnson', 'bobjohnson', 'passwordefgh', 'patient', NULL),
(5, 'Faiz', 'aslam', '123', 'nurse', NULL),
(6, 'Azka Chanda', 'azka', '456', 'patient', NULL),
(7, 'Insan Taufik', 'insan', 'insan123', 'patient', NULL),
(8, 'Insan Gencana', 'insanT', '$2b$12$xVNi.Y49i1vdm9dAFEEYCu2gZVDUpvSOV1vpcdGowHoadMMNmDXKS', 'nurse', NULL),
(9, 'Insan 1', 'insan1', '$2b$12$Ixj9LLw7i/Y17SdS4pwSteChFSzPnV1uQ/cBR7DsOlg8QozqAl2Pm', 'nurse', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJyb2xlIjoibnVyc2UiLCJuYW1lIjoiSW5zYW4gMSIsImV4cCI6MTcxODY4NzczOS4yNzQ2NTU2LCJ0eXBlIjoicmVmcmVzaCJ9.bvCGkKvxzzQfrvaxC-T2XwBxFR-STCtBD631QP79wdE'),
(10, 'insan2', 'insan2', '$2b$12$Mmehkgk56rodlQ8iwGT/gePEOKCcOg0am5iy2dNvgN.Vo9Lo7NnYy', 'nurse', NULL),
(11, 'insan3', 'insan3', '$2b$12$VPIz0nOXitOIkEuo2Ml4teYmnTm7t49EEo.7k/m1qjiwacj3bhbuG', 'nurse', NULL),
(12, 'insan4', 'insan4', '$2b$12$2eJDpWJZmi68X/f4aFDYhOq4P6v5UCUFPCX9/MVFnmS9jjbe8Zcv.', 'nurse', NULL),
(13, 'insan5', 'insan5', '$2b$12$7VVdZWSwtKvzbv3GpIaOKOaOUTl/.wOCoITS2Pc0xn/ZOcI3OMRFa', 'nurse', NULL),
(14, 'Insan Taufik 1', 'insantaufik1', '$2b$12$Mt8MuEUyt.gjjzcD9MH.yeJ/gyE1D75QqYit4d0ObD1SgZM3rjGjG', 'nurse', NULL),
(15, 'InsanTaufik', 'insang', '$2b$12$HArc.jv5DSwPR1..eB7opeEdAwQA47OaYjYlioLQ/4LtKV2VK3xay', 'patient', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNSwicm9sZSI6InBhdGllbnQiLCJuYW1lIjoiSW5zYW5UYXVmaWsiLCJleHAiOjE3MTg2OTIwMzcuODQ3Nzg1LCJ0eXBlIjoicmVmcmVzaCJ9.gYdE0g1ADcLfVtfNRnx1XaXtuqTIsdJDmqDv6V9ZFzg'),
(5190, 'Muhamad Insan Taufik', 'insan123', '$2b$12$Y/Bdi16pafjKXAfS/JNxJ.3Z7j7ndF4FSz0qZ0f1E2APG6reeP.zK', 'nurse', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1MTkwLCJyb2xlIjoibnVyc2UiLCJuYW1lIjoiTXVoYW1hZCBJbnNhbiBUYXVmaWsiLCJleHAiOjE3MTgyNTYzMDkuMTkwMjI2OCwidHlwZSI6InJlZnJlc2gifQ.VuRzebrDEfsGbOyBihHm_9LmcLcbe6xaECJoQd7HZTQ'),
(5191, 'Muhamad Insan Taufik', 'insang1', '$2b$12$Qho3yI3mRVOCjcDDLZHvyuK3lkznhpOy0dOKkoUyY5ICapuauxnrC', 'patient', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1MTkxLCJyb2xlIjoicGF0aWVudCIsIm5hbWUiOiJNdWhhbWFkIEluc2FuIFRhdWZpayIsImV4cCI6MTcxODY5MjcwNC43NjQwNTUzLCJ0eXBlIjoicmVmcmVzaCJ9.ygETsL2vLWRau-gK4_cT_h2e92oV6AC_P9x5u0QJRAU');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diseases`
--
ALTER TABLE `diseases`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `konsultasi`
--
ALTER TABLE `konsultasi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `disease_id` (`disease_id`),
  ADD KEY `nurse_id` (`nurse_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `management_janji_id` (`management_janji_id`) USING BTREE;

--
-- Indexes for table `management_janji`
--
ALTER TABLE `management_janji`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nurse_id` (`nurse_id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diseases`
--
ALTER TABLE `diseases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `konsultasi`
--
ALTER TABLE `konsultasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `management_janji`
--
ALTER TABLE `management_janji`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5192;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `konsultasi`
--
ALTER TABLE `konsultasi`
  ADD CONSTRAINT `konsultasi_ibfk_1` FOREIGN KEY (`disease_id`) REFERENCES `diseases` (`id`),
  ADD CONSTRAINT `konsultasi_ibfk_2` FOREIGN KEY (`nurse_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `konsultasi_ibfk_3` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `konsultasi_ibfk_4` FOREIGN KEY (`management_janji_id`) REFERENCES `management_janji` (`id`);

--
-- Constraints for table `management_janji`
--
ALTER TABLE `management_janji`
  ADD CONSTRAINT `nurse_id` FOREIGN KEY (`nurse_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `patient_id` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

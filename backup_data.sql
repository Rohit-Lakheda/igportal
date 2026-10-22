-- MySQL dump 10.13  Distrib 9.6.0, for macos26.2 (arm64)
--
-- Host: localhost    Database: ig2026
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'c82048e4-082b-11f1-adde-83b91744128b:1-277';

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add consultation',7,'add_consultation'),(26,'Can change consultation',7,'change_consultation'),(27,'Can delete consultation',7,'delete_consultation'),(28,'Can view consultation',7,'view_consultation'),(29,'Can add Designation',8,'add_designationmaster'),(30,'Can change Designation',8,'change_designationmaster'),(31,'Can delete Designation',8,'delete_designationmaster'),(32,'Can view Designation',8,'view_designationmaster'),(33,'Can add event',9,'add_event'),(34,'Can change event',9,'change_event'),(35,'Can delete event',9,'delete_event'),(36,'Can view event',9,'view_event'),(37,'Can add Group',10,'add_groupmaster'),(38,'Can change Group',10,'change_groupmaster'),(39,'Can delete Group',10,'delete_groupmaster'),(40,'Can view Group',10,'view_groupmaster'),(41,'Can add observer request',11,'add_observerrequest'),(42,'Can change observer request',11,'change_observerrequest'),(43,'Can delete observer request',11,'delete_observerrequest'),(44,'Can view observer request',11,'view_observerrequest'),(45,'Can add sig member',12,'add_sigmember'),(46,'Can change sig member',12,'change_sigmember'),(47,'Can delete sig member',12,'delete_sigmember'),(48,'Can view sig member',12,'view_sigmember'),(49,'Can add sig profile',14,'add_sigprofile'),(50,'Can change sig profile',14,'change_sigprofile'),(51,'Can delete sig profile',14,'delete_sigprofile'),(52,'Can view sig profile',14,'view_sigprofile'),(53,'Can add sig observer',13,'add_sigobserver'),(54,'Can change sig observer',13,'change_sigobserver'),(55,'Can delete sig observer',13,'delete_sigobserver'),(56,'Can view sig observer',13,'view_sigobserver'),(57,'Can add user profile',15,'add_userprofile'),(58,'Can change user profile',15,'change_userprofile'),(59,'Can delete user profile',15,'delete_userprofile'),(60,'Can view user profile',15,'view_userprofile'),(61,'Can add Research specific topic',16,'add_researchspecifictopic'),(62,'Can change Research specific topic',16,'change_researchspecifictopic'),(63,'Can delete Research specific topic',16,'delete_researchspecifictopic'),(64,'Can view Research specific topic',16,'view_researchspecifictopic'),(65,'Can add Research paper',17,'add_researchpaper'),(66,'Can change Research paper',17,'change_researchpaper'),(67,'Can delete Research paper',17,'delete_researchpaper'),(68,'Can view Research paper',17,'view_researchpaper'),(69,'Can add Open source contribution',18,'add_opensourcecontribution'),(70,'Can change Open source contribution',18,'change_opensourcecontribution'),(71,'Can delete Open source contribution',18,'delete_opensourcecontribution'),(72,'Can view Open source contribution',18,'view_opensourcecontribution'),(73,'Can add Open source project',19,'add_opensourceproject'),(74,'Can change Open source project',19,'change_opensourceproject'),(75,'Can delete Open source project',19,'delete_opensourceproject'),(76,'Can view Open source project',19,'view_opensourceproject'),(77,'Can add Research broad topic',20,'add_researchbroadtopic'),(78,'Can change Research broad topic',20,'change_researchbroadtopic'),(79,'Can delete Research broad topic',20,'delete_researchbroadtopic'),(80,'Can view Research broad topic',20,'view_researchbroadtopic');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `capacity_building_profiles`
--

DROP TABLE IF EXISTS `capacity_building_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `capacity_building_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `linkedin_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `biography` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `testimonial` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `fields_of_work` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Column 16` int DEFAULT NULL,
  `programme` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `research_topic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `about` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `cohort` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cohort_duration` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `report` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capacity_building_profiles`
--

LOCK TABLES `capacity_building_profiles` WRITE;
/*!40000 ALTER TABLE `capacity_building_profiles` DISABLE KEYS */;
INSERT INTO `capacity_building_profiles` VALUES (1,'Himaja Chanda','Himaja Linkedin','Himaja is an Electronics and Communication Engineering student with strong interest in internet governance and digital infrastructure. \nAs part of the first cohort of the NIXI internship program, she contributed to research, reporting, and awareness activities, \ngaining hands-on exposure to how internet systems and policies support inclusive digital growth.','Himaja is an Electronics and Communication Engineering student with strong interest in internet governance and digital infrastructure. \nAs part of the first cohort of the NIXI internship program, she contributed to research, reporting, and awareness activities, \ngaining hands-on exposure to how internet systems and policies support inclusive digital growth.',NULL,NULL,NULL,NULL,'Dhanekula Institute of engineering and technology ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Himaja_Chanda.jpeg','2026-01-21 09:59:57'),(2,'Vasu Paul Srikar','Vasu Paul Srikar LinkedIn','Vasu Paul Srikar is an Engineering student, Researcher, and IEEE volunteer with a strong interest in strengthening India’s digital and internet infrastructure.He has actively worked on projects at the intersection of signal processing, embedded systems, and AI.                                                                                                                                    As an IEEE Student Member, he has contributed to technical education, membership growth, and the organization of national-level events.                                                                                His research explores cyber resilience and internet governance, notably focusing on the structural challenges of digital commons.                                                                                               Srikar is passionate about building secure, resilient, and inclusive internet systems aligned with India’s digital public infrastructure goals','My journey with NIXI has been truly transformative. It provided me with my first opportunity to publish a research paper, marking a significant milestone in my academic career. Through NIXI, I received my first stipend, which not only supported my work but also strengthened my confidence as a researcher. I also had the privilege of being part of my first international fellowship, an experience that broadened my global perspective on internet governance and digital infrastructure. Attending multiple conferences enabled me to learn directly from experts, exchange ideas, and build lasting professional relationships. Most importantly, NIXI helped me connect with inspiring peers and mentors, allowing me to form meaningful friendships across India and grow both personally and professionally.',NULL,NULL,NULL,NULL,'Sri Venkateswara College of Engineering','1','17th March to 30th June 2025',NULL,'uploads/capacity/Vasu_Paul_Srikar.jpeg','2026-01-21 09:59:57'),(3,'Arin Anil Kamble','www.linkedin.com/in/arin-kamble-8b06132a1','Arin Kamble is a research-oriented engineering student with a strong interest in Internet governance, Universal Acceptance, and digital inclusion. Through hands-on research and evaluation projects, Arin has worked on assessing website readiness for Email Address Internationalization, contributing to data-driven reports that highlight barriers to multilingual Internet access. His experience through national and international research initiatives has helped him develop a practical understanding of how Internet infrastructure, technical standards, and policy frameworks intersect to support inclusive digital growth.','My internship at NIXI has been an incredible journey of growth and learning, It has strengthened my understanding of the Internet Governance landscape while helpingme develop both technical and professional skills. Coming from a small town, this opportunity allowed me to collaborate with industry experts and contribute tomeaningful projects. The mentorship and guidance I received have played an important role in shaping my career aspirations. I am truly grateful to have been part of this enriching experience at NIXI.',NULL,NULL,NULL,NULL,'Dr. Babasaheb Ambedkar Technological University ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Arin_Anil_Kamble.jpeg','2026-01-21 09:59:57'),(4,'SANJAY K K','www.linkedin.com/in/sanjay-k-k-423aaa273','Sanjay K K is an Electronics and Communication Engineering student with interests in IoT, Internet systems, and understanding how technology works in real life. He has explored DNS and the .in domain through academic work and gained practical exposure during his internship at NIXI. An active IEEE member, he is also an author and compiler of anthologies, combining technical curiosity with creative expression.','My internship at NIXI as an Internet Governance Intern was a valuable learning experience. I learned how the internet works behind the scenes, particularly the management and significance of the .in domain. Through sessions on DNS, ICANN, IANA, and IRINN, I gained a clearer understanding of internet governance at national and global levels. Interacting with experienced professionals made the learning process engaging and deepened my interest in the internet ecosystem.',NULL,NULL,NULL,NULL,'K S Rangasamy College of Technology','1','17th March to 30th June 2025',NULL,'uploads/capacity/SANJAY_K_K.jpeg','2026-01-21 09:59:57'),(5,'Joysa Kaushik','JK Linkedin profile','Joysa Kaushik is a Computer Science and Cyber Security student pursuing an integrated B.Tech. M.Tech. degree at the National Forensic Sciences University, Delhi Campus. She is a recipient of various national and international fellowships and affiliations, including APNG17, APAN60, APIGA India etc. She is currently working at the Forensic Science Laboratory, Govt. of NCT Delhi, as a Cyber Forensics Intern, gaining hands-on experience in digital investigations and cybercrime analysis.','My internship experience with NIXI has been extremely enriching and impactful. It provided me with valuable exposure to India’s internet infrastructure ecosystem, particularly in areas related to domain management, internet governance, and cybersecurity implementation. The work environment at NIXI is professional, collaborative, and learning oriented, allowing interns to engage meaningfully with real world policy and technology driven challenges.',NULL,NULL,NULL,NULL,'National Forensic Sciences University','1','17th March to 30th June 2025',NULL,'uploads/capacity/Joysa_Kaushik.jpeg','2026-01-21 09:59:57'),(6,'Chandru P P','https://www.linkedin.com/in/chandru-pp-69b62627a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app','I am an Electronics and Communication Engineering student with a strong interest in embedded systems, networking, and emerging technologies. I am passionate about learning through practical projects, research, and hands-on experience, and I continuously work on improving my technical skills and problem-solving abilities.',NULL,NULL,NULL,NULL,NULL,'K S Rangaswamy College of Technology ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Chandru_P_P.jpeg','2026-01-21 09:59:57'),(7,'Sakamuri Prem Sai','https://linkedin.com/in/prem-sai-sakamuri','Prem Sai is an Electronics and Communication Engineering undergraduate with a strong interest in internet governance, internet infrastructure, and digital public systems. During his internship at NIXI, he has been actively involved in initiatives related to Universal Acceptance and national awareness programs aimed at strengthening India’s internet ecosystem. With a solid foundation in communication systems and networking, he is keen on understanding how policy, standards, and engineering come together to build a secure, inclusive, and resilient internet.','The mentorship and guidance received throughout the internship helped me strengthen my analytical thinking, technical understanding, and policy perspective. This internship has significantly contributed to my professional growth and has reinforced my interest in working at the intersection of technology, governance, and national digital infrastructure. I am grateful to NIXI for the opportunity and highly recommend this internship to students aspiring to contribute to India’s digital and cybersecurity landscape.',NULL,NULL,NULL,NULL,'Marri Laxman Reddy Institute of Technology and Management ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Sakamuri_Prem_Sai.jpeg','2026-01-21 09:59:57'),(8,'Aqdar Faruh','www.linkedin.com/in/aqdar-faruh-88075b296','Aqdar Faruh is an Electronics and Communication Engineer with postgraduate training in advanced technologies and certification in Quantum Computing and Machine Learning from IIT Delhi. He has professional experience as an Internet Governance Intern at the National Internet Exchange of India, contributing to multistakeholder processes and research on post-quantum cryptography. His research interests span Information Security Management Systems, post-quantum-ready digital infrastructure, and the policy and institutional frameworks governing emerging technologies.','My internship experience has been deeply engaging and insightful. It offered a well-rounded blend of intellectual growth and professional development, enriching my understanding of the Internet Governance ecosystem and its intersections with policy, innovation, and evolving digital landscapes. The supportive mentorship, insightful sessions, and opportunities for close interaction with global industry leaders and experts significantly strengthened my research, analytical, and collaborative skills. I now feel confident navigating complex digital challenges and contributing meaningfully to multistakeholder discussions. This experience has inspired a sustained commitment to advancing a secure, inclusive, and future-ready digital ecosystem.',NULL,NULL,NULL,NULL,'Panimalar Engineering College','1','17th March to 30th June 2025',NULL,'uploads/capacity/Aqdar_Faruh.jpeg','2026-01-21 09:59:57'),(9,'Niharika K','https://www.linkedin.com/in/kallaguntaniharika/','I am an Electronics and Communication Engineering (ECE) student passionate about IoT and emerging technologies. During my internship at NIXI (National Internet Exchange of India), I explored the backbone of the internet by studying internet infrastructure, domain name systems, and digital governance, gaining a deeper understanding of how these systems enable secure, scalable, and connected solutions.','My internship at NiiXi was a highly enriching experience. During this time, I completed my project, developed and enhanced a variety of skills, and contributed to meeting and paper reports. The constant guidance and support from my mentor helped me navigate challenges, learn effectively, and gain valuable hands-on experience. This internship has significantly strengthened my professional knowledge and confidence.',NULL,NULL,NULL,NULL,'Dhanekula Institute of Engineering and Technology','1','17th March to 30th June 2025',NULL,'uploads/capacity/Niharika_K.jpeg','2026-01-21 09:59:57'),(10,'Kushagra Singh','https://www.linkedin.com/in/kushagrasinghh','Kushagra Singh is a cybersecurity and internet governance enthusiast, actively engaged in policy, digital trust, and emerging technology discussions. He has contributed to national and regional internet governance initiatives, worked closely with multistakeholder communities, and is involved in research and advocacy around data protection, privacy, and responsible technology use. Kushagra also leads and organizes tech and policy-focused events, fostering youth participation in the internet ecosystem.','My internship at NIXI was a highly enriching experience that provided me with valuable exposure to India’s internet infrastructure and governance ecosystem. I had the opportunity to work closely with professionals on policy, domain name systems, and internet governance initiatives, which strengthened my understanding of multistakeholder collaboration and public-interest technology. The supportive mentorship and practical learning environment at NIXI made this internship both insightful and impactful, and it has significantly shaped my interest in digital policy and internet governance.',NULL,NULL,NULL,NULL,'National Forensic Sciences University','1','17th March to 30th June 2025',NULL,'uploads/capacity/Kushagra_Singh.jpeg','2026-01-21 09:59:57'),(11,'Parth Narendra Gaikwad','www.linkedin.com/in/parth-narendra-gaikwad','Parth Narendra Gaikwad is a B.Tech graduate whose interest in the Internet extends beyond its use to the systems, institutions, and people that quietly sustain it. Through close engagement with experienced professionals in the Internet ecosystem, he has developed a grounded understanding of how technical infrastructure, governance, and long-term responsibility intersect. Known for his clarity of thought and curiosity-driven learning, he values collaborative environments and aims to contribute to a secure, inclusive, and resilient Internet with a strong sense of public purpose.','My internship at the National Internet Exchange of India (NIXI) was an exceptional learning experience that allowed me to gain insights directly from some of the most experienced professionals in the Internet infrastructure and governance ecosystem. Working alongside highly knowledgeable colleagues and receiving guidance from outstanding mentors gave me a deep, practical understanding of Internet governance, IP resource management, IPv6 deployment, and routing security. Learning in an environment where expertise, clarity, and collaboration were central helped me appreciate the responsibility involved in maintaining a secure, stable, and globally coordinated Internet.\nWhat truly set this internship apart was the culture of mentorship and peer learning. Thoughtful discussions, constructive feedback, and exposure to real-world challenges enabled me to think beyond theory and develop a more analytical, disciplined, and long-term perspective. This experience has significantly strengthened my professional maturity and reinforced my motivation to contribute meaningfully to the Internet ecosystem. I am sincerely grateful to NIXI for providing not just an internship, but a community of mentors and colleagues who made the learning experience truly impactful.\n\n',NULL,NULL,NULL,NULL,'National Institute of Electronics and Information Technology','1','17th March to 30th June 2025',NULL,'uploads/capacity/Parth_Narendra_Gaikwad.jpeg','2026-01-21 09:59:57'),(12,'Aditya Bakshi ',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Rajiv Gandhi Institute of Petroleum Technology ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Aditya_Bakshi_.jpeg','2026-01-21 09:59:57'),(13,'Rupam Barui','https://www.linkedin.com/in/codetrident/','Rupam Barui is a computer science graduate specializing in cybersecurity, with a strong focus on Internet Governance, digital security, and ethical technology. He has actively participated in regional and global forums such as Youth IGF, APrIGF, inSIG, APAN, and WSIS-related discussions, contributing to policy development, security working groups, and youth statements. Rupam has experience in cyber threat research, AI-driven security systems, and network security, and is currently engaged with the National Internet Exchange of India (NIXI). He is passionate about fact-checking, platform accountability, and building secure, inclusive digital infrastructure while sharing knowledge within his community','My internship at the National Internet Exchange of India (NIXI) was a highly enriching and formative experience. It provided me with practical exposure to India’s Internet infrastructure ecosystem, including Internet Governance, DNS operations, and cybersecurity at a national scale.\nThrough this internship, I gained valuable insights into policy discussions, technical coordination, and the role of multistakeholder collaboration in strengthening a secure and resilient Internet. The mentorship, guidance, and collaborative environment at NIXI enabled me to bridge the gap between academic knowledge and real-world implementation.\nThis experience has significantly shaped my understanding of Internet infrastructure and reinforced my interest in cybersecurity, governance, and public-interest technology. I am grateful to NIXI for the opportunity and support, and I will carry these learnings forward in my professional journey.',NULL,NULL,NULL,NULL,'National Forensic Sciences University ','1','17th March to 30th June 2025',NULL,'uploads/capacity/Rupam_Barui.jpeg','2026-01-21 09:59:57'),(28,'Shaurya Sarna ','Link for Linked in ','Shaurya Sarna is a technology enthusiast with a strong interest in cybersecurity, internet infrastructure, and DNS operations. He completed an internship at the National Internet Exchange of India (NIXI), where he gained exposure to how domain name systems function and how internet infrastructure is managed to ensure stability and security. During this experience, he developed an understanding of the role of internet governance and the importance of maintaining trust and reliability across digital systems. Shaurya is currently a student at the University of Petroleum and Energy Studies (UPES), Dehradun, where he is pursuing his studies in computer science and building a solid foundation in networking, systems, and security concepts. His academic journey, combined with his internship experience, has strengthened his analytical thinking and shaped his interest in pursuing a career in cybersecurity and internet technologies.','Testimonial of Shaurya Sarna@NIXI ',NULL,NULL,NULL,NULL,'UPES DEHRADUN','2','1st July to 30th September 2025',NULL,'uploads/capacity/Shaurya_Sarna_.jpeg','2026-01-21 10:03:35'),(29,'Devaanshi Singh','Linkedin Profile ','Devaanshi Singh is a public policy professional with experience in technology governance, internet policy, and the digital economy. At the National Internet Exchange of India (NIXI), she worked with the Internet Governance Division on global internet governance research, supporting India’s engagement in ICANN public consultations and WSIS-related processes. Her work included research on subsea cable governance and critical digital infrastructure, executive briefing support, and coordination for multistakeholder forums. She also served as Liaison Officer for the India Internet Governance Forum (IIGF). Devaanshi holds a Master’s degree from St. Xavier’s College, Mumbai.','My internship at NIXI significantly expanded my understanding of the depth and complexity of internet governance and the institutional, technical, and policy layers that shape the functioning of the global internet. Engaging with real-world policy challenges, international governance processes, and multistakeholder forums offered insights that go well beyond theoretical frameworks. Through hands-on research, policy analysis, and coordination work, I developed a more nuanced appreciation of how technical infrastructure, regulatory decision-making, and stakeholder interests intersect in practice. The experience strengthened my research, communication, and coordination skills, while reinforcing my interest in contributing to a secure, inclusive, and resilient digital ecosystem. I am grateful for the mentorship and institutional exposure provided by NIXI.',NULL,NULL,NULL,NULL,'St. Xavier\'s College, Mumbai','2','1st July to 30th September 2025',NULL,'uploads/capacity/Devaanshi_Singh.jpeg','2026-01-21 10:03:35'),(30,'Kartik Verma ','Linkedin Profile ','Kartik Verma is a cybersecurity enthusiast who is interested in understanding how the internet works in practice. He completed an internship at the National Internet Exchange of India (NIXI), where he worked on a DNS-related project that helped him learn how domain name systems function and why they are important for a safe and reliable internet. Through this experience, he gained a clear understanding of NIXI’s role in managing and supporting India’s internet ecosystem. He is currently pursuing an integrated BTech–MTech degree at the National Forensic Sciences University (NFSU). The internship strengthened his understanding of internet infrastructure, improved his analytical thinking, and deepened his interest in cybersecurity and internet governance, shaping his academic learning and future career goals.','Testimonial of Kartik verma ',NULL,NULL,NULL,NULL,'NFSU , Delhi ','2','1st July to 30th September 2025',NULL,'uploads/capacity/Kartik_Verma_.jpeg','2026-01-21 10:03:35'),(31,'Balaji K','LinkedIn','Balaji is a policy and advocacy consultant and a legal professional with expertise in a unique blend of research on Law, technology, regulatory governance, and digital policy.\n\nAt the National Internet Exchange of India (NIXI) Internet Governance Internship & Capacity Building Scheme, he specialised in evidence-based policy development, with a focus on digital inclusion, internet governance frameworks, and critical digital infrastructure. He provided analytical inputs to the WSIS+20 and the Internet Governance Forum (IGF) and engaged in multi-stakeholder consultations with MeitY, ICANN, and IETF.\n\nAs a Master of Public Policy, his research, including \"Decoding Digital Fiscalism: Quantifying Internet Outage Impacts on GST revenue in India (2018-23)\", leverages advanced econometrics and policy analysis. He is also an Advocate (Attorney-at-Law) with experience in drafting and representing clients in corporate governance matters.','The NIXI Internet Governance Internship and Capacity Building Programme provided a transformative experience in digital policy and internet governance. I gained foundational knowledge from leading organisations and engaged with experts in the field, attending key fellowships and international conferences. The program emphasised understanding and applying complex concepts, allowing interns to analyse significant topics such as WSIS+20 action lines and participate in multistakeholder consultations. My research into the security dynamics of the undersea cable ecosystem enhanced my experience, solidifying my passion for digital inclusion and regulatory mechanisms. I am grateful towards the NIXI team and mentors for this invaluable opportunity, making it a highly recommended choice for those looking to impact digital policy.',NULL,NULL,NULL,NULL,'IIT Tirupati','2','1st July to 30th September 2025',NULL,'uploads/capacity/Balaji_K.jpeg','2026-01-21 10:03:35'),(32,'Harshit Srivastava','Linkedin','Harshit Srivastava is a postgraduate student of Public Policy, Law and Governance at IIT Kharagpur, with a background in Electronics and Instrumentation Engineering. He interned at the National Internet Exchange of India (NIXI) under MeitY, where he worked on internet governance, facilitated stakeholder engagements aligned with ICANN/ISOC frameworks, and led policy research on energy efficiency in APAC data centers. His broader interests include technology policy, digital governance, climate policy, and space law, and he is a published author on space debris liability.','My internship at the National Internet Exchange of India (NIXI) was a transformative experience that significantly deepened my understanding of internet governance and digital policy. Working at the core of India’s internet infrastructure exposed me to the institutional, technical, and policy layers that shape the global internet. During the internship, I engaged with real-world policy challenges, international governance processes, and multistakeholder forums, including events such Rise of FOSS, and consultations related to WSIS. These engagements offered insights far beyond theoretical frameworks and highlighted how technical infrastructure, regulatory decision-making, and diverse stakeholder interests intersect in practice. Through hands-on research, policy analysis, and coordination work—including research on internet infrastructure security—I strengthened my research, communication, and coordination skills, while developing a nuanced appreciation of inclusive and secure digital ecosystems. I am deeply grateful to my mentor and the NIXI team for their guidance and institutional exposure, which reinforced my commitment to contributing to a resilient, inclusive, and well-governed digital future.',NULL,NULL,NULL,NULL,'IIT Kharagpur','2','1st July to 30th September 2025',NULL,'uploads/capacity/Harshit_Srivastava.jpeg','2026-01-21 10:03:35'),(33,'Shivalika Das','Linkedin','Shivalika Das is a Master’s student in Public Policy, Law and Governance at the Indian Institute of Technology Kharagpur, with an interdisciplinary academic background spanning public policy and life sciences. Her interests lie in digital governance, technology policy, sustainability, and data-driven policy analysis.\n\nShe has gained experience in Internet governance and capacity-building initiatives through her engagement with the National Internet Exchange of India (NIXI) under MeitY, where she contributed to sessions following ICANN and ISOC trainings and worked on a research project focused on building sustainable and energy-efficient data centres in India. Her academic and research work also includes policy evaluation, comparative analysis, and the use of quantitative and qualitative methods for governance assessment.\n\nShivalika has authored and co-authored research papers on climate change, displacement, and legal accountability, published in Jus Corpus Law Journal. She is currently working on policy lab projects related to smart governance and municipal service delivery. She aspires to contribute to evidence-based policymaking at the intersection of digital infrastructure, sustainability, and public institutions.','My internship at the National Internet Exchange of India (NIXI) offered an exceptional opportunity to engage closely with the practical dimensions of internet governance and digital policy. Being embedded within a key national internet institution allowed me to understand how global governance principles are translated into domestic policy and operational frameworks.\n\nThe internship enabled me to participate in multistakeholder consultations, policy discussions, and industry engagements, including forums related to Free and Open Source Software (FOSS) and the World Summit on the Information Society (WSIS). These experiences highlighted the complex interplay between technical infrastructure, regulatory processes, and stakeholder coordination in governing the internet.\n\nThrough focused research, policy analysis, and coordination work—particularly on issues related to internet infrastructure security—I developed stronger analytical, communication, and institutional engagement skills. I am grateful to the NIXI team and my mentor for their guidance and support, which reinforced my interest in contributing to a secure, inclusive, and resilient digital ecosystem',NULL,NULL,NULL,NULL,'IIT Kharagpur','2','1st July to 30th September 2025',NULL,'uploads/capacity/Shivalika_Das.jpeg','2026-01-21 10:03:35'),(34,'Rishabh','LinkedIn','Rishabh Singh is a computer science and artificial intelligence student with a strong interest in internet governance, digital public infrastructure, and technology policy at scale. He has participated as a fellow at the Asia Pacific Regional Internet Governance Forum (AprIGF 2025) and APAN61 in Dhaka, Bangladesh, where he engaged in regional discussions on digital governance, IPv6 adoption, network readiness, and the future of internet infrastructure in the Asia-Pacific region. His work spans both technical and policy domains, including research on IPv6 readiness and secure network migration strategies, which he presented at APAN61. Rishabh is currently pursuing a five-year Integrated M.Tech in Computer Science and Artificial Intelligence at Rajiv Gandhi Institute of Petroleum Technology (RGIPT), maintaining a strong academic record while actively contributing to technical research, policy-oriented forums, and capacity-building initiatives at the intersection of technology and governance.','The NIXI Internet Governance Internship and Capacity Building Programme was a highly enriching experience that strengthened my understanding of digital policy and internet governance. The programme offered valuable exposure to leading organisations and experts through structured learning, fellowships, and participation in international conferences. It focused on both conceptual clarity and practical application, enabling interns to engage with complex issues such as WSIS+20 action lines and multistakeholder consultation processes. My research on the security and governance aspects of the undersea cable ecosystem further deepened my engagement and reinforced my interest in digital inclusion and regulatory frameworks. I am sincerely grateful to the NIXI team and mentors for their guidance and support, and I would strongly recommend this programme to anyone aspiring to contribute meaningfully to digital policy.',NULL,NULL,NULL,NULL,'RGIPT Amethi','2','1st July to 30th September 2025',NULL,'uploads/capacity/Rishabh.jpeg','2026-01-21 10:03:35'),(35,'Mitali Raj','LinkedIn','Mitali Raj is a researcher with a background in machine learning and data science, with interests in internet infrastructure and digital governance. She interned at the National Internet Exchange of India (NIXI) under MeitY, where she worked on internet governance–related initiatives and research focused on strengthening core internet infrastructure. She has also led collaborative research teams through open research programs such as the EleutherAI SOAR initiative. Her broader interests include internet resilience, responsible AI, and data-driven approaches to policy and infrastructure development.','My internship at the National Internet Exchange of India (NIXI) was a highly enriching experience that provided me with valuable exposure to internet governance and core internet infrastructure in India. The program offered a unique opportunity to understand how policy, technology, and stakeholder coordination come together to strengthen the internet ecosystem.Working alongside experienced professionals, I gained insights into the functioning of IXPs, digital governance frameworks, and capacity-building initiatives. The collaborative environment at NIXI encouraged learning, critical thinking, and meaningful contributions, making the internship both intellectually rewarding and professionally impactful.',NULL,NULL,NULL,NULL,'NFSU , Delhi ','2','1st July to 30th September 2025',NULL,'uploads/capacity/Mitali_Raj.jpeg','2026-01-21 10:03:35'),(36,'Jai Shree Tiwari','LinkedIn','Jai Shree Tiwari is a software developer with experience in mobile architecture, network automation, and fintech systems. At the National Internet Exchange of India (NIXI), she worked on critical digital infrastructure projects, focusing on the technical assessment of India\'s internet security landscape. Her work included engineering Python-based automation scripts to map and analyze secure DNS servers (DoH, DoT, DoQ) and verifying protocol compliance across the network. Currently, she serves as an Associate Software Developer at Lark Finserv Pvt. Ltd., where she develops scalable financial technology solutions. She holds a background in Electronics & Computer Engineering.','My internship at NIXI was a pivotal deep dive into the protocol layer of the internet. I focused my research on analyzing network standards and secure communication protocols, assessing their efficacy in the context of India\'s internet exchange infrastructure. This technical research went beyond abstract concepts, requiring me to dissect how protocols impact latency, security, and interoperability. The experience significantly upgraded my technical competency in network analysis and gave me a concrete understanding of the architectural decisions that shape the future of the internet.',NULL,NULL,NULL,NULL,'Dronacharya College of Engineering, Gurgaon','2','1st July to 30th September 2025',NULL,'uploads/capacity/Jai_Shree_Tiwari.jpeg','2026-01-21 10:03:35'),(37,'Sarvjeet Pal','LinkedIn','Sarvjeet Pal, is a student of public policy at the School of Public Policy, IIT Delhi. He is specialising in science, technology and innovation policy. As an internet governance and capacity building intern at National Internet Exchange of India, he worked at the intersection of Registrar’s Accreditation Agreement and Domain Name System. \n',' As an internet governance and capacity building intern at National Internet Exchange of India. I took a deep dive into the internet governance ecosystem by attending different conferences, sessions and policy discussions around the same. As part of the internship I worked on analyzing the Registrar’s Accreditation Agreement (RAA) and their suitability as per the market. I drafted a detailed research article addressing the market concerns and giving a clarity on the intent of the latest amendments in the RAA. The experience at NIXI was full of learning and it helped me to figure out my niche interest in technology policy.',NULL,NULL,NULL,NULL,'IIT Delhi','2','1st July to 30th September 2025',NULL,'uploads/capacity/Sarvjeet_Pal.jpeg','2026-01-21 10:03:35'),(38,'Navneet Kaur','Linkedin','Navneet Kaur is an Electronics and Communication Engineering student at Swami Keshvanand Institute of Technology (SKIT), Jaipur. She has a strong academic interest in communication systems, networking, and emerging technologies. She successfully completed her internship under the second cohort of the National Internet Exchange of India (NIXI), where she gained practical exposure to internet infrastructure, internet governance, and related technical frameworks. Through this experience, she developed a deeper understanding of national-level internet operations and policy-driven technological implementation, complementing her engineering education with valuable industry-oriented insights.',NULL,NULL,NULL,NULL,NULL,'SKIT jaipur','2','1st July to 30th September 2025',NULL,'uploads/capacity/Navneet_Kaur.jpeg','2026-01-21 10:03:35'),(39,'Anchal Yadav','Linkedin','Anchal is a legal professional and advocate with interest in the intersection of law, technology policy, internet governance, and digital policy. Her areas of focus also include intellectual property, arbitration, and digital regulatory frameworks.At the National Internet Exchange of India (NIXI), she was associated with the Internet Governance Division, contributing to policy research linked to ICANN policy consultations and WSIS processes. Additionally her work focused on domain name dispute frameworks such as INDRP and UDRP, domain name-related trademark infringement (cybersquatting), and domain name misuse, along with data protection compliance. Her research addressed jurisdictional and accountability concerns in registrar obligations and domain name governance. She also served as Liaison Officer for the India Internet Governance Forum (IIGF).','My internship at the National Internet Exchange of India (NIXI) gave me practical exposure to the internet governance space through research and analysis of domain name related issues. I worked on studying the Registrar Accreditation Agreement (RAA), domain abuse, and the functioning of the domain name ecosystem from a legal and policy perspective. The experience helped me better understand how law and policy operate in real governance settings and strengthened my interest in technology policy. I am grateful for the mentorship and institutional exposure provided by NIXI.',NULL,NULL,NULL,NULL,'NLU Lucknow','2','1st July to 30th September 2025',NULL,'uploads/capacity/Anchal_Yadav.jpeg','2026-01-21 10:03:35'),(40,'Richa Sinha','https://www.linkedin.com/in/richa-sinha-02','I am an aspiring public policy professional with background in advocacy for youth empowernment and climate justice and program designing. I am now exploring the field of Internet Governance to bridge the gap of how technology can be used to scale programs, enhance amplification for climate risk mitigation initiatives and to strengthen public delivery system. My internship at NIXI helped in shaping my understanding of the internet’s societal impact through policy learning and community outreach.','Before joining this internship, the internet was simply a tool for me, one that connected people and made the world feel like a small village. Through interactive sessions conducted during the internship, my perspective evolved, and I began to see the internet as a powerful resource actively reshaping the world. I realized its potential to be used for a higher purpose, especially in creating public good. This internship became a reflective turning point for me that helped me identify my interest in Public Policy. Learning about the multistakeholder model highlighted how equitable and inclusive internet governance can be and I wish to use these learnings in future. Additionally, through outreach sessions where I interacted with audiences who were largely unaware of how the internet works behind the scenes was both empowering and deeply fulfilling.',NULL,NULL,NULL,NULL,'Shaheed Sukhdev College of Business Studies, University of Delhi','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Richa_Sinha.jpeg','2026-01-21 10:05:16'),(41,'Lavanya SJ ','www.linkedin.com/in/lavanya-sj-6232452aa','I am an ECE graduate with basic knowledge of computer networking concepts such as OSI, TCP/IP, DNS, and routing protocols. I am passionate about building a career in networking and continuously learning new technologies.','This internship transformed my perspective on how technology impacts real-life applications. The interactive sessions and practical assignments enhanced my problem-solving abilities and strengthened my foundation in core concepts. It played an important role in shaping my professional goals and inspired me to continue learning and growing in the tech domain.',NULL,NULL,NULL,NULL,'JNNCE College shimoga , Karnataka ','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Lavanya_SJ_.jpeg','2026-01-21 10:05:16'),(42,'Saurab Das','Linkedin','A Final-year B.Tech ECE student having strong foundation in Linux systems with a deep interest in emerging technologies specially on network and system security. Actively learning security concepts and committed to securing the internet.','Through the NIXI Internet Governance Internship, I gained an indepth understanding of core internet concepts and the critical role policies play in ensuring the smooth functioning of the internet ecosystem. I learned how different stakeholders: government bodies, technical communities, and organizations collaborate to make the internet more secure and resilient. NIXI helped me connect technical concepts with policy frameworks and understand how these policies work together. Additionally, my communication and public speaking skills were strengthened through outreach sessions, where I interacted with diverse audiences.',NULL,NULL,NULL,NULL,'Gurukul Kangri\n(Deemed to be University)\nHaridwar, Uttarakhand','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Saurab_Das.jpeg','2026-01-21 10:05:16'),(43,'Jasbir ','www.linkedin.com/in/jasbir-yadav-398bb7251','I am a dedicated and detail-oriented law student at\nMaharshi Dayanand University, Rohtak, with a strong\nand growing interest in Technology Law,\nIntellectual Property Rights (IPR), \nCyber Law, and Internet Governance. \nMy academic journey and internship experiences \nhave helped me develop practical skills in \nlegal research, policy analysis, contract drafting, \nand regulatory compliance within the digital legal ecosystem.\n','I demonstrated strong dedication and professionalism during my internship with the National Internet Exchange of India (NIXI). I learned about Internet Governance, Cyber Law, and Digital Policy, and actively contributed to research, documentation, and outreach activities. I also understand complex regulatory and technical concepts, communicate them in simple language, and engage with students and stakeholders during awareness programs. I also displayed sincerity, discipline, and a proactive learning attitude throughout the internship.  It was a great experience for me to become familiar with technology law, policy, and digital governance.\n',NULL,NULL,NULL,NULL,'Maharshi Dayanand University, Rohtak','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Jasbir_.jpeg','2026-01-21 10:05:16'),(44,'Shashank Mani Tripathi','https://www.linkedin.com/in/shashank-tripathi-595b6a335','I am an ECE graduate with growing specialization in cyber security, focussing on network security, secure communications, and threat mitigation. Passionate about protecting digital infrastructure and building a career in cyber defense and information security','During my NIXI internship, I gained hands-on exposure to IXPs and internet governance through research on network optimisation and traffic efficiency. I also improved my communication skills and personality by interacting and engaging with students and stakeholders during awareness programs. This experience enhanced my skills in networking and policy. ',NULL,NULL,NULL,NULL,'KIET Group of Institutions, Ghaziabad','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Shashank_Mani_Tripathi.jpeg','2026-01-21 10:05:16'),(45,'Omkareshwar Jha ','Omkareshwar Jha - Infusion X | LinkedIn','I am a Polymath with my Btech in CSE. I love to explore creative as well as the innovative path. Researching and reading are my passion. ','It\'s been a great experience. Meeting with such diverse background people Where everyone is working under one NIXI umbrella. There was lot to learn. Got chance to build valuable connections. Good vibe for research and freedom to think in creative and innovative manner. I am glad that i choose to join and good opportunity being selected for internship.',NULL,NULL,NULL,NULL,'Maharishi Dayanand University ','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Omkareshwar_Jha_.jpeg','2026-01-21 10:05:16'),(46,'Ankul Prajapati','https://www.linkedin.com/in/ankul-prajapati-0a3256247?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app','I am currently a fourth-year student at the National Law Institute University, Bhopal, pursuing the B.Sc.L.L.B (Cyber Security). My academic training equips me with a strong foundation in core law subjects prescribed by the BCCI, alongside a practical understanding of technology, data protection and cyber risk management. Through my coursework and research, I have developed a good understanding of compliance and regulatory frameworks such as the GDPR, DPDPA, CCPA, HIPAA, etc and international information security standards, including ISO/IEC 27001, 27002, and 27005 etc as well as the NIST framework. This interdisciplinary exposure enables me to analyse legal issues at the intersection of law, technology and regulatory compliance.','Coming from a law background, I initially wondered how I’d fit into the technical world of internet infrastructure. But at NIXI, the environment is incredibly supportive. I’ve had the chance to work alongside brilliant engineering interns from every corner of the country. This mix of legal and technical minds has been amazing, I’ve learned so much about how the internet actually works and the complex structures that keep it running. My core research has been on integrating Blockchain into the DNS ecosystem. It’s been a rewarding challenge to see how decentralisation can strengthen our digital security. A massive highlight was representing NIXI at AISS 2025. It was there that I realized how our technical and policy work directly aligns with India’s national cybersecurity goals. NIXI doesn\'t just give you a desk; they give you a platform. I’m now moving forward as a \'NIXI Internet Influencer\'.',NULL,NULL,NULL,NULL,'National Law Institute University, Bhopal','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Ankul_Prajapati.jpeg','2026-01-21 10:05:16'),(47,'Silambaraselvan R','https://www.linkedin.com/in/silambaraselvan-r/','As a passionate and dedicated cybersecurity student, I bring a unique blend of practical experience and academic knowledge to each project I undertake. With a keen eye for design and a steadfast commitment to security.','From being an everyday internet user to gaining structured exposure to internet governance, the internship at the National Internet Exchange of India (NIXI) marked a significant transition from simply using the internet to understanding how it is governed, secured, and sustained at a national scale. The internship provided clear insight into the foundations of internet governance, Domain Name System (DNS) operations, DNS Security Extensions (DNSSEC), and the critical role NIXI plays in managing India’s internet infrastructure.\n\nThis experience transformed abstract concepts about internet functionality and security into practical, real-world understanding. It highlighted how policy, technical controls, and national-level initiatives work together to ensure a secure, resilient, and trustworthy internet ecosystem, reinforcing the importance of governance in the broader digital landscape.',NULL,NULL,NULL,NULL,'Dhanalakshmi Srinivasan College of Engineering and Technology','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Silambaraselvan_R.jpeg','2026-01-21 10:05:16'),(48,'Adarsh Sahu',NULL,'Coming from a law background, I initially wondered how I’d fit into the technical world of internet infrastructure. But at NIXI, the environment is incredibly supportive. I’ve had the chance to work alongside brilliant engineering interns from every corner of the country. This mix of legal and technical minds has been amazing, I’ve learned so much about how the internet actually works and the complex structures that keep it running.My core research has been on integrating Blockchain into the DNS ecosystem. It’s been a rewarding challenge to see how decentralization can strengthen our digital security. A massive highlight was representing NIXI at AISS 2025. It was there that I realized how our technical and policy work directly aligns with India’s national cybersecurity goals.',NULL,NULL,NULL,NULL,NULL,'National Law Institute University, Bhopal','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Adarsh_Sahu.jpeg','2026-01-21 10:05:16'),(49,'Ashmit Chauhan ',NULL,'My internship at NIXI under Cohort 3 was a highly fruitful and enriching experience. It provided me with practical exposure to India’s internet governance ecosystem, particularly in areas such as domain name infrastructure, policy frameworks, and digital public goods. Through hands-on assignments, expert-led sessions, and collaborative discussions, I developed a clearer understanding of how technical, legal, and policy dimensions intersect in managing critical internet resources. The internship also strengthened my research, analytical, and professional communication skills, while offering valuable mentorship and networking opportunities. Overall, the NIXI Cohort 3 internship significantly enhanced my academic and career orientation in the field of digital governance.',NULL,NULL,NULL,NULL,NULL,'National Law Institute University, Bhopal','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Ashmit_Chauhan_.jpeg','2026-01-21 10:05:16'),(50,'J.Gunadeep Lakshmi Sayeesh','https://www.linkedin.com/in/javvadi-gunadeep-lakshmi-sayeesh-805a3632a/','I\'m GunadeepLS, an Electronics and Communication Engineering (ECE) student with a strong passion for software engineering. \nIn my free time, I focus on building technical skills, learning modern development tools, and working on practice projects to grow\n into a professional software engineer.Currently, I focus on learning software development fundamentals, practicing front-end design techniques, and \nbuilding small projects to improve my coding skills, logical thinking, and problem-solving abilities.','The internship at the National Internet Exchange of India (NIXI) gave me a clear understanding of Internet governance, DNS infrastructure, and how the domain name ecosystem works in practice. By working on research tasks and taking part in outreach programs, I learned how technology, policy, and cybersecurity connect in real-world situations. The guidance and support I received helped me improve my research approach, technical writing, and analytical thinking. Overall, this internship helped me move beyond classroom learning and prepared me to handle real industry-level responsibilities with more confidence.',NULL,NULL,NULL,NULL,'Dhanekula Institute of engineering and technology , Vijayawada','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/J.Gunadeep_Lakshmi_Sayeesh.jpeg','2026-01-21 10:05:16'),(51,'Dhruv Garg','https://www.linkedin.com/in/dhruv-garg-449996244/','Aspiring software developer with a strong focus on artificial intelligence and robotics. Currently pursuing a B.Tech in Artificial Intelligence and Machine Learning while actively enhancing software development skills to address technological challenges.','I had the privilege of completing my internship with the National Internet Exchange of India (NIXI), and it was a highly enriching and professionally rewarding experience. The internship provided me with valuable exposure to India’s internet infrastructure, domain name ecosystem, and internet governance framework. During the program, I gained a deeper understanding of how national internet exchanges operate, how domain and DNS systems are managed, and how policies are framed to ensure a secure, stable, and inclusive internet.',NULL,NULL,NULL,NULL,'ADGIPS','3','13th October 2025 to 6th January 2026',NULL,'uploads/capacity/Dhruv_Garg.jpeg','2026-01-21 10:05:16'),(52,'Adamya Dabral ','www.linkedin.com/in/adamya-dabral19','Final-year B.Tech CSE student at GB Pant DSEU, passionate about cloud computing and data systems. Seeking to apply my skills in real-world projects and grow by building impactful tech solutions.',NULL,NULL,NULL,NULL,NULL,'GB PANT DSEU','4','Ongoing',NULL,'uploads/capacity/Adamya_Dabral_.jpeg','2026-01-21 10:08:21'),(53,'Aditya Ratn Bharti','https://www.linkedin.com/in/aditya-r-bharti/','I\'m a Final-year B.Tech CSE student with strong interest in front-end web applications and UI/UX, currently learning backend devlopment.',NULL,NULL,NULL,NULL,NULL,'JIMS Management Technical Campus, GN U.P.','4','Ongoing',NULL,'uploads/capacity/Aditya_Ratn_Bharti.jpeg','2026-01-21 10:08:21'),(54,'Anita','https://www.linkedin.com/in/anita-hooda-6b2b6b2a3','I’m a final-year B.Tech CSE student with a strong interest in computer networks and hands-on experience through a UI development internship with IBM SkillsBuild, where I worked on creating intuitive, user-friendly interfaces and strengthening my practical technical skills.',NULL,NULL,NULL,NULL,NULL,'Guru Jambheshwar University Science & Technology, Hisar','4','Ongoing',NULL,'uploads/capacity/Anita.jpeg','2026-01-21 10:08:21'),(55,'Deeksha Agarwal','linkedin.com/in/deekshaagarwal5587','I am a B.Com LL.B. graduate, having keen interest in public policy and governance.',NULL,NULL,NULL,NULL,NULL,'Banasthali Vidyapith, Rajasthan','4','Ongoing',NULL,'uploads/capacity/Deeksha_Agarwal.jpeg','2026-01-21 10:08:21'),(56,'Kaushal Asiwal','www.linkedin.com/in/kaushal-asiwal-ece','An NSUTian who loves to learn and get things done. Years of writing C, C++, JavaScript and Python for fun and for grades, plus late nights in competitive coding, web apps and impactful machine-learning projects, have given me the confidence to tackle pretty much any tech problem that lands on my desk.',NULL,NULL,NULL,NULL,NULL,'Netaji Subhas University Of Technology(NSUT)','4','Ongoing',NULL,'uploads/capacity/Kaushal_Asiwal.jpeg','2026-01-21 10:08:21'),(57,'Maahi Raghuvanshi','https://www.linkedin.com/in/maahi-raghuvanshi-3777062b4','Final Year BTech CSE student having keen interest in cyber secruity with hands on knowledge of linux and kali linux done for penetration testing ',NULL,NULL,NULL,NULL,NULL,'DCRUST University ,(GIET)','4','Ongoing',NULL,'uploads/capacity/Maahi_Raghuvanshi.jpeg','2026-01-21 10:08:21'),(58,'Nikhil Mathur','https://www.linkedin.com/in/nikhilmathur2018/','Full-Stack Developer with MERN & Django expertise and telecom engineering background, currently interning at NIXI (4th Cohort) while bridging web development and internet infrastructure.',NULL,NULL,NULL,NULL,NULL,'Radharaman Institute of Research and Technology, Bhopal','4','Ongoing',NULL,'uploads/capacity/Nikhil_Mathur.jpeg','2026-01-21 10:08:21'),(59,'Pranav Mittal','https://www.linkedin.com/in/pranav-mittal-a710962b9/','I am final year Electronics and Communication Engineering undergraduate with hands-on experience in ATC systems, IoT-based projects, and research published in IEEE. Skilled in Arduino, ESP32, Python, and cloud integration, with strong problem-solving and communication abilities.',NULL,NULL,NULL,NULL,NULL,'Amity University Noida, U.P.','4','Ongoing',NULL,'uploads/capacity/Pranav_Mittal.jpeg','2026-01-21 10:08:21'),(60,'RAGINI KANUNGO','https://www.linkedin.com/in/ragini-kanungo-472524202/','Qualified advocate with interest in technology law and policy. Experienced in legal research and drafting. ',NULL,NULL,NULL,NULL,NULL,'University of Cambridge & GGSIP University','4','Ongoing',NULL,'uploads/capacity/RAGINI_KANUNGO.jpeg','2026-01-21 10:08:21'),(61,'Satyam Katiyar','https://www.linkedin.com/in/satyam-katiyar-a48bb4255/','Final-year B.Tech (Electronics & Communication, Class of 2026). Full-stack web developer — React, Node.js, Express, MongoDB; experienced with auth & REST APIs; proficient in C++, Python and DSA',NULL,NULL,NULL,NULL,NULL,'Gurukula Kangri University, Haridwar','4','Ongoing',NULL,'uploads/capacity/Satyam_Katiyar.jpeg','2026-01-21 10:08:21'),(62,'Shashank Mani Tripathi ','https://www.linkedin.com/in/shashank-tripathi-595b6a335','I am a BTech graduate in ECE with keen interest in cyber security and networking',NULL,NULL,NULL,NULL,NULL,'KIET Group of Institution, Ghaziabad ','4','Ongoing',NULL,'uploads/capacity/Shashank_Mani_Tripathi_.jpeg','2026-01-21 10:08:21'),(63,'Sidhant Chaku','LinkedIn','Final year B.Tech student pursueing CSE Specialisation in Data Science. I have hands-on experience in making ML models using python and recently I have developed interest in internet governance and cyber security field. ',NULL,NULL,NULL,NULL,NULL,'VIT Vellore','4','Ongoing',NULL,'uploads/capacity/Sidhant_Chaku.jpeg','2026-01-21 10:08:21'),(64,'T Vijay','https://www.linkedin.com/in/t-vijay-a22aa626a/','I am a final-year Electronics and Communication Engineering student at Amity University, Noida. I have worked on projects related to embedded systems and Al during my internships at IIT Delhi and IIT Indore',NULL,NULL,NULL,NULL,NULL,'Amity University Noida, U.P.','4','Ongoing',NULL,'uploads/capacity/T_Vijay.jpeg','2026-01-21 10:08:21'),(65,'Utkarsh Pratap Maurya','https://www.linkedin.com/in/utkarsh-pratap-maurya-132389269',NULL,NULL,NULL,NULL,NULL,NULL,'Shri Ramswaroop Memorial College of Engineering','4','Ongoing',NULL,'uploads/capacity/Utkarsh_Pratap_Maurya.jpeg','2026-01-21 10:08:21'),(66,'Utkarsh Sharma','https://www.linkedin.com/in/utkarsh-sharma-3ab258267/','Me being a B.Tech CSE (Data Science) student with hands-on experience in Computer Vision, Machine Learning. Interned at ISRO–LEOS, Bengaluru, in which worked upon BEV mapping, depth estimation, YOLO-based perception, and A* path planning for autonomous navigation. Have a key interest in autonomous systems, NLP chatbots and modern AI frameworks.',NULL,NULL,NULL,NULL,NULL,'JSS Academy of Technical Education, Noida','4','Ongoing',NULL,'uploads/capacity/Utkarsh_Sharma.jpeg','2026-01-21 10:08:21'),(67,'Vaishnavi','www.linkedin.com/in/vaishnavi--gautam','Final Year student of BTech CSE with specialization in Cyber security, have done previuous internships on Ethical Hacking and Have Interned At GPCSSI (Haryana Police), Have a kneen intrest in Risk Advisory and GRC ',NULL,NULL,NULL,NULL,NULL,'Kurukshetra University, (PIET)','4','Ongoing',NULL,'uploads/capacity/Vaishnavi.jpeg','2026-01-21 10:08:21');
/*!40000 ALTER TABLE `capacity_building_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultation_comments`
--

DROP TABLE IF EXISTS `consultation_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultation_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultation_id` int NOT NULL,
  `user_id` int NOT NULL,
  `organization` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `designation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'Pending',
  `document_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultation_comments`
--

LOCK TABLES `consultation_comments` WRITE;
/*!40000 ALTER TABLE `consultation_comments` DISABLE KEYS */;
INSERT INTO `consultation_comments` VALUES (1,5,12,NULL,NULL,'hi this is test','2026-01-16 08:10:29','Approved',NULL),(2,5,12,NULL,NULL,'hello hello hello','2026-01-16 08:11:21','Approved',NULL),(3,3,12,NULL,NULL,'Proposed GNSO Process for ICANN Board to Reverse Adoption of GNSO Policy Recommendations','2026-01-16 08:21:35','Approved',NULL),(4,4,12,'National internet exchange of india','Team leader','asdfasdf\r\nasdfasdfasdf','2026-01-16 08:56:08','Approved','/events/SIG%20Page-%20IG%20Portal_upHPPhY.docx'),(5,1,12,'test','test','test','2026-01-23 06:42:04','Approved','/events/NIXIEX2526-1358.pdf'),(6,6,12,'QA Team','Reviewer','Verification Test - Optional Document Attachment.','2026-03-11 08:06:12','Approved',NULL),(7,7,12,'NIXI','QA','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scramb','2026-03-24 09:00:57','Approved',NULL);
/*!40000 ALTER TABLE `consultation_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_consultation`
--

DROP TABLE IF EXISTS `core_consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_consultation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `closes_on` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_consultation`
--

LOCK TABLES `core_consultation` WRITE;
/*!40000 ALTER TABLE `core_consultation` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_designationmaster`
--

DROP TABLE IF EXISTS `core_designationmaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_designationmaster` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_designationmaster`
--

LOCK TABLES `core_designationmaster` WRITE;
/*!40000 ALTER TABLE `core_designationmaster` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_designationmaster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_event`
--

DROP TABLE IF EXISTS `core_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_event` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `event_datetime` datetime(6) NOT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `join` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `flyer` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_event`
--

LOCK TABLES `core_event` WRITE;
/*!40000 ALTER TABLE `core_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_groupmaster`
--

DROP TABLE IF EXISTS `core_groupmaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_groupmaster` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_groupmaster`
--

LOCK TABLES `core_groupmaster` WRITE;
/*!40000 ALTER TABLE `core_groupmaster` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_groupmaster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_observerrequest`
--

DROP TABLE IF EXISTS `core_observerrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_observerrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sig` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `work_experience` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `linkedin` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submitted_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_observerrequest`
--

LOCK TABLES `core_observerrequest` WRITE;
/*!40000 ALTER TABLE `core_observerrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_observerrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_opensourcecontribution`
--

DROP TABLE IF EXISTS `core_opensourcecontribution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_opensourcecontribution` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` int unsigned NOT NULL,
  `title` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `summary` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `contribution_file` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `external_url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contributor_display_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contributor_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contributor_account_id` int DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_opensourcecontr_project_id_986d4363_fk_core_open` (`project_id`),
  CONSTRAINT `core_opensourcecontr_project_id_986d4363_fk_core_open` FOREIGN KEY (`project_id`) REFERENCES `core_opensourceproject` (`id`),
  CONSTRAINT `core_opensourcecontribution_chk_1` CHECK ((`version` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_opensourcecontribution`
--

LOCK TABLES `core_opensourcecontribution` WRITE;
/*!40000 ALTER TABLE `core_opensourcecontribution` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_opensourcecontribution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_opensourceproject`
--

DROP TABLE IF EXISTS `core_opensourceproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_opensourceproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposed_by_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposed_by_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `broad_topic_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_opensourceproject_broad_topic_id_slug_be13bcc7_uniq` (`broad_topic_id`,`slug`),
  KEY `core_opensourceproject_slug_fedffcbd` (`slug`),
  CONSTRAINT `core_opensourceproje_broad_topic_id_11d6558b_fk_core_rese` FOREIGN KEY (`broad_topic_id`) REFERENCES `core_researchbroadtopic` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_opensourceproject`
--

LOCK TABLES `core_opensourceproject` WRITE;
/*!40000 ALTER TABLE `core_opensourceproject` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_opensourceproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_researchbroadtopic`
--

DROP TABLE IF EXISTS `core_researchbroadtopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_researchbroadtopic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(220) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  CONSTRAINT `core_researchbroadtopic_chk_1` CHECK ((`sort_order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_researchbroadtopic`
--

LOCK TABLES `core_researchbroadtopic` WRITE;
/*!40000 ALTER TABLE `core_researchbroadtopic` DISABLE KEYS */;
INSERT INTO `core_researchbroadtopic` VALUES (1,'Domain Names','domain-names','',10,1,'2026-03-29 10:04:43.658915'),(2,'Internet Protocols','internet-protocols','',20,1,'2026-03-29 10:04:43.670375'),(3,'Standards','standards','',30,1,'2026-03-29 10:04:43.673023'),(4,'AI and Emerging Tech','ai-and-emerging-tech','',40,1,'2026-03-29 10:04:43.674431'),(5,'NIXI and India-specific','nixi-and-india-specific','',50,1,'2026-03-29 10:04:43.675748');
/*!40000 ALTER TABLE `core_researchbroadtopic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_researchpaper`
--

DROP TABLE IF EXISTS `core_researchpaper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_researchpaper` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` int unsigned NOT NULL,
  `title` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abstract` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `document` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_nixi_intern` tinyint(1) NOT NULL,
  `internship_batch_or_year` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submitter_display_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submitter_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submitter_account_id` int DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `reviewed_at` datetime(6) DEFAULT NULL,
  `specific_topic_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_researchpaper_specific_topic_id_3c9f6bc7_fk_core_rese` (`specific_topic_id`),
  CONSTRAINT `core_researchpaper_specific_topic_id_3c9f6bc7_fk_core_rese` FOREIGN KEY (`specific_topic_id`) REFERENCES `core_researchspecifictopic` (`id`),
  CONSTRAINT `core_researchpaper_chk_1` CHECK ((`version` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_researchpaper`
--

LOCK TABLES `core_researchpaper` WRITE;
/*!40000 ALTER TABLE `core_researchpaper` DISABLE KEYS */;
INSERT INTO `core_researchpaper` VALUES (1,1,'Launching new LLM','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Let','research/papers/2026/03/mml-book.pdf',1,'2020','jainvaibhav415@gmail.com','test2@nixi.in',12,'approved','2026-03-29 10:09:15.401237','2026-03-29 10:16:52.746262',1),(2,2,'Update on LLM','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n\r\nWhy do we use it?\r\nIt is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using \'Content here, content here\', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for \'lorem ipsum\' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like','research/papers/2026/03/Kyle_Simpson-All-6.pdf',1,'2022','jainvaibhav415@gmail.com','test2@nixi.in',12,'approved','2026-03-29 10:19:02.854530','2026-03-29 10:19:10.419198',1),(3,1,'ML Statstics','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scr','research/papers/2026/04/Kyle_Simpson-All-6.pdf',1,'2020','Vaibhav','test2@nixi.in',12,'approved','2026-04-09 11:09:23.152033','2026-04-09 11:10:29.447937',2);
/*!40000 ALTER TABLE `core_researchpaper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_researchspecifictopic`
--

DROP TABLE IF EXISTS `core_researchspecifictopic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_researchspecifictopic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposed_by_email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposed_by_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `broad_topic_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_researchspecifictopic_broad_topic_id_slug_328d9187_uniq` (`broad_topic_id`,`slug`),
  KEY `core_researchspecifictopic_slug_bf093b59` (`slug`),
  CONSTRAINT `core_researchspecifi_broad_topic_id_16768898_fk_core_rese` FOREIGN KEY (`broad_topic_id`) REFERENCES `core_researchbroadtopic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_researchspecifictopic`
--

LOCK TABLES `core_researchspecifictopic` WRITE;
/*!40000 ALTER TABLE `core_researchspecifictopic` DISABLE KEYS */;
INSERT INTO `core_researchspecifictopic` VALUES (1,'ML Math','ml-math','approved','test2@nixi.in','jainvaibhav415@gmail.com','2026-03-29 10:09:15.317966',4),(2,'ML Operation','ml-operation','approved','test2@nixi.in','Vaibhav','2026-04-09 11:09:23.120601',4);
/*!40000 ALTER TABLE `core_researchspecifictopic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sigmember`
--

DROP TABLE IF EXISTS `core_sigmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_sigmember` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `designation_id` bigint NOT NULL,
  `group_id` bigint NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `core_sigmember_designation_id_26a68fc6_fk_core_desi` (`designation_id`),
  KEY `core_sigmember_group_id_58e7b587_fk_core_groupmaster_id` (`group_id`),
  CONSTRAINT `core_sigmember_designation_id_26a68fc6_fk_core_desi` FOREIGN KEY (`designation_id`) REFERENCES `core_designationmaster` (`id`),
  CONSTRAINT `core_sigmember_group_id_58e7b587_fk_core_groupmaster_id` FOREIGN KEY (`group_id`) REFERENCES `core_groupmaster` (`id`),
  CONSTRAINT `core_sigmember_user_id_4d5e7d02_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sigmember`
--

LOCK TABLES `core_sigmember` WRITE;
/*!40000 ALTER TABLE `core_sigmember` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sigmember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sigobserver`
--

DROP TABLE IF EXISTS `core_sigobserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_sigobserver` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sig` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `work_experience` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `linkedin` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sigobserver`
--

LOCK TABLES `core_sigobserver` WRITE;
/*!40000 ALTER TABLE `core_sigobserver` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sigobserver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_sigprofile`
--

DROP TABLE IF EXISTS `core_sigprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_sigprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sig_role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mobile_number` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `core_sigprofile_user_id_9cdfe193_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_sigprofile`
--

LOCK TABLES `core_sigprofile` WRITE;
/*!40000 ALTER TABLE `core_sigprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_sigprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_userprofile`
--

DROP TABLE IF EXISTS `core_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_dashboard_user` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `created_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `core_userprofile_created_by_id_fd2ec7f1_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `core_userprofile_created_by_id_fd2ec7f1_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_userprofile_user_id_5141ad90_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_userprofile`
--

LOCK TABLES `core_userprofile` WRITE;
/*!40000 ALTER TABLE `core_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'core','consultation'),(8,'core','designationmaster'),(9,'core','event'),(10,'core','groupmaster'),(11,'core','observerrequest'),(18,'core','opensourcecontribution'),(19,'core','opensourceproject'),(20,'core','researchbroadtopic'),(17,'core','researchpaper'),(16,'core','researchspecifictopic'),(12,'core','sigmember'),(13,'core','sigobserver'),(14,'core','sigprofile'),(15,'core','userprofile'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-08 15:34:10.913401'),(2,'auth','0001_initial','2026-01-08 15:34:12.021829'),(3,'admin','0001_initial','2026-01-08 15:34:12.250238'),(4,'admin','0002_logentry_remove_auto_add','2026-01-08 15:34:12.271704'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-08 15:34:12.282568'),(6,'contenttypes','0002_remove_content_type_name','2026-01-08 15:34:12.454013'),(7,'auth','0002_alter_permission_name_max_length','2026-01-08 15:34:12.592191'),(8,'auth','0003_alter_user_email_max_length','2026-01-08 15:34:12.655210'),(9,'auth','0004_alter_user_username_opts','2026-01-08 15:34:12.667048'),(10,'auth','0005_alter_user_last_login_null','2026-01-08 15:34:12.752518'),(11,'auth','0006_require_contenttypes_0002','2026-01-08 15:34:12.752518'),(12,'auth','0007_alter_validators_add_error_messages','2026-01-08 15:34:12.786591'),(13,'auth','0008_alter_user_username_max_length','2026-01-08 15:34:12.912277'),(14,'auth','0009_alter_user_last_name_max_length','2026-01-08 15:34:13.020709'),(15,'auth','0010_alter_group_name_max_length','2026-01-08 15:34:13.055869'),(16,'auth','0011_update_proxy_permissions','2026-01-08 15:34:13.084355'),(17,'auth','0012_alter_user_first_name_max_length','2026-01-08 15:34:13.208857'),(18,'core','0001_initial','2026-01-08 15:34:14.099320'),(19,'core','0002_sigobserver','2026-01-08 15:34:14.150290'),(20,'core','0003_userprofile','2026-01-08 15:34:14.305044'),(21,'core','0004_rename_is_admin_panel_user_userprofile_is_dashboard_user_and_more','2026-01-08 15:34:14.683329'),(22,'core','0005_alter_event_options_rename_date_event_event_datetime_and_more','2026-01-08 15:34:14.984136'),(23,'core','0006_alter_sigmember_user_delete_customuser','2026-01-08 15:34:15.049703'),(24,'sessions','0001_initial','2026-01-08 15:34:15.129097'),(25,'core','0007_research_module','2026-03-29 10:04:43.967145');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('04mlfqi1l001gx609p0e8ftpom1mz9w8','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1voGjX:1DczuylOW5hbME4s-EaL6J33-9KatSm7cmd-cSJi9rc','2026-02-06 08:58:31.858619'),('0g1rq55azbwqplvoy7lbr9gdoc6xovj1','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vginw:SH1pri12ysZyd1nhYSgGqKTCqc50BA3Pay1_xU3i88U','2026-01-16 13:19:52.284955'),('0nrehy7iahz1gy8wsbs0w8or8b2im5zr','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1w4xFb:dCpEVXrVscmp4lHCGdwg-Y9nCp41vXIvcZXtjf4x5ZI','2026-03-24 09:36:35.329684'),('0w0k5lzybcjailmugwq32xc7tvx4v7t3','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vgguE:JRYHeNabvxFV2099-K7-xIPXjELKSDmSqbE20tHQvTM','2026-01-16 11:18:14.089737'),('2cc54c3k6tu3o3pqcj0wyn2a9h8nk0fm','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vyp1h:66y4QeRQabxzoMEiib7YHAzDv4NQOHFvh7HfYMrfKb4','2026-03-07 11:36:53.622415'),('2qbcmpzzc99myo1vjquh3qjb02i5egod','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1ve8vq:h25mwEqOrQYBM1sA4unTC1IF-9CWGiisIQ2rkkT61x8','2026-01-09 10:37:22.189361'),('353ys489b39p4dcvxprmey44of941vbg','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vgHbW:DlikIlcV6Jiz3_K0SbHfmgMaDo7_UjD5aQtVpYHoaZw','2026-01-15 08:17:14.255855'),('3l60c534aupz5zmy6jyxqcn5gt3q57ln','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1w6n1e:PHLLiZvyqCKWqq0Pgt5WNSG8wZlCa42ixI64xrxwn3A','2026-03-29 11:05:46.808073'),('5trc1h5j2kmq2sizmqse9yhrbm5iu0i7','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vzZlf:RLrRJHiXC_UWjdd3_hsOnn9lIIBBdE0NtnaVxQ00R2c','2026-03-09 13:31:27.830594'),('6y0zhkil6rpcu1n545kfzg3r6zwcwh7g','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vzCRn:rTVsA2cKXpCWlHevUnxnRl9rND_5JpKfTYuxj2EIaZU','2026-03-08 12:37:23.949611'),('79pb3avkzthrmsfbp7t2j55a434f56ue','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfYO9:p_HsLJfMmDXp3WPHQKHQeDEkRLltupcWkhYPWrPLeuE','2026-01-13 08:00:25.903751'),('7hzwjl8p63bc9tams1o0ouzeto5p4p4u','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1ve4qr:SPIzrdZ9cR2ltlJPTj_g-0otF_jOP-tn5rwMwyawm1E','2026-01-09 06:15:57.473040'),('7kcdnnb6shlh4xuyuluuqjndgc63drb3','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vjArF:1a3d0LqG1AaQif35hmYdyIAzl5ib29iGjpYoX0jnYVo','2026-01-23 07:41:25.021905'),('8stz9ht4o2zlh71czvll3fj4n2m5lwmx','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vq2Gf:kzfC6pLVy-PSGuEXaxtwPL1hAbkNlKB1wVyOnGPJlG8','2026-02-11 05:56:01.577060'),('asztdy1zey5f2aiykspua39dcp88fznp','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1w0aVx:BXJ2lTRuhpR4PejOMIkNfNDPJ7oJyAqmBTSwKWoQEQM','2026-03-12 08:31:25.916447'),('baogekiq97tiosm3ynyna3u2wni4f0td','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vgLe2:t3O8Qg_cPYdZ_QFi7ZJhkrJlks1QUSEVdstvnA-4V9s','2026-01-15 12:36:06.027538'),('dcqeecfundminpv9q4hnz23tcjqdhr36','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfZgW:CRkAudko5P_j8y4jwRxKxzX75OoV8Ui733KhD6kmrII','2026-01-13 09:23:28.352290'),('de6m3564z4xuqx9cekdfuqh7ct2bqkx7','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vq6TC:zVhGwHPaTl9ODAMyRQhxz5DJx3ClSJpdAGN-dgQzuOY','2026-02-11 10:25:14.555586'),('e0g0ant1i1k2stgnz7b9ks0b5kc4wyuf','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vgMaf:fUYhKtRWQV4tc0or9mTgiGErF0INPktZvFFrJV-G67k','2026-01-15 13:36:41.666834'),('fky55ypjv2ek8oo8ces5y9i7q6koa3e7','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfasA:Mv6YGceOHqmPGuqCABFfbB-nt3rsksvIFbeEVoNhJb0','2026-01-13 10:39:34.708817'),('fm1eioti36itx1m4kr9cc9khahteyj22','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vdssQ:1oZQb844mfEtzlpdGuyTB9SjnCL6j8pwzOn-pKtQK8w','2026-01-08 17:28:46.737042'),('hggpuwbire4s4yyoqpd9uagzqfds86cz','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfcAt:KEuLYQ48qhMGAY5ZgLD1pXSOEazcpdGQOtROpYWGLmI','2026-01-13 12:02:59.703757'),('jj4wqq3llex6prp2wis3fftoum1piq5i','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vxe6M:IPcY8tnDubiT8AsfCk9Bpowb-hwDWAoEKAwtCdx8wWM','2026-03-04 05:44:50.617896'),('knqj2ze1q3idokfrlv8n40bzaa3ucngx','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vqZPw:rxcdXV0iS8fV2qtVFoTEawFetWFwMIU9CJ7vU6WwxQc','2026-02-12 17:19:48.930498'),('lo73er3q9ftdxldrnyklkk92kblus4qf','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfx8F:2YamFtBeUj2sCWmEgY-L0CS8oLFiazz4pwxRX-pPZNw','2026-01-14 10:25:39.462902'),('m338mlpih5uty9rls8pn9t9d7hjq71cd','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vyQJ8:9ugxtAMK19b3Mup5x387eQng3_H2AxKVavXpiE-jpG8','2026-03-06 09:13:14.276732'),('md66dtw7uhyqd5szjk41oxse5skpilvf','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vgcuO:PhxcJ6PzRAFo3wuehdicrJqy5Cmvn2lanLY2tVHF7Fg','2026-01-16 07:02:08.621266'),('nipw7p8kkiafkc6lbo7rqkwjr6q1kl58','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vzXzS:cx1_-xnUYCbKmDBEo4eUwXF_rYZ_Kf_Wj7wu1uSb5Tk','2026-03-09 11:37:34.951761'),('nova6g0z2g9b1gakkppbiqgaqsax9t24','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vkhZP:CPXheLRzzJCOcT7vBOifxzxRyORy7a-ppmx687AYC0E','2026-01-27 12:49:19.560757'),('nuvu61zd3m8dkq86feg4kehatr2ky6x3','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vpKch:GpKHBlEeKKy_UwBHB5DgzRlCEaJ2-K_SL68-IRNjzH0','2026-02-09 07:19:51.777173'),('nxequqy88nn6roctpfu4dwf3yz0p2bz2','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vg2ml:OD0MWHfkzr11-eIlFK9L6bCyTcKngFpLskFgs_yqF7M','2026-01-14 16:27:51.553662'),('ofy8zqrmjz66w0zhsda2zgygo08yfmyf','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vyna0:YCggomCxzuN7xIZuyVQZK8dzTUO5aAcoorVin3bTPCY','2026-03-07 10:04:12.600993'),('qogggh199g0kf2y7qsru8e4t6lgeopji','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1wAnEl:RE9lrQ50KeCa7VJKKGtmSbSRczjqcsifyX3JSfsp12g','2026-04-09 12:07:51.683842'),('qpx4vx5t3gcv8yx28x3r1xiu2l1jahs6','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1w0EgG:VV7GqTgQ4IZXecwkQttano5LUWiJSdZS5qf3Lc0wpiA','2026-03-11 09:12:36.794580'),('r397aknwcmx6elq714muosgmhou3tm6w','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfuUE:0ebRDVr5r1hDJJ7iub6zWOgGrNhcVO-ruZPP4JFQvLA','2026-01-14 07:36:10.729549'),('rq94t4a6hw3lyop38xxryf9kq3fw0s32','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfL4X:HUWi9j46Q3MV2U-xwbUsSqSrDzKPS2sf--z9__JLOVw','2026-01-12 17:47:17.193299'),('sbix2q8bf3curhk36v37w3nzoaphixih','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1voIYd:EPND0olwTctH1FTlYnKokSo8OaCDSAd7PyLN_qNsKiQ','2026-02-06 10:55:23.105452'),('sg5dlkdaqk1buty9gm5pjgznlia5l7nh','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vymdN:yXFd0GQ7q_0Ll__gwZXj0f8db7PbC9o4wRppv-LRV5o','2026-03-07 09:03:37.057660'),('tcbsn0vtw2p3klfmqnyrbf9gascux4ws','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1w6n3J:CZkL-rsCZHoT_m5uunbFH8nR8_8XmywtGINytC2bQqk','2026-03-29 11:07:29.945055'),('u85znbxsatagg4mzimubfhuwr3gx8ofm','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vpln6:l2Kfpec27VCrK8k__keeHQyP0Ccn9gbAWX8QVynPdKY','2026-02-10 12:20:24.763731'),('v2j4cj2uygch1qtrdhd3snchl4xod76u','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfFgI:dPDndKg0XBfNP1DYzZSQ9OyW843Zk9okswnOsLv_8oQ','2026-01-12 12:01:54.127382'),('vqyndaqt257slau9nvqtcfljqiztny3i','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfK6r:ew9qrPtfbX-jKMZKwelFxofP6okaDgBCo6Itbh2LQPA','2026-01-12 16:45:37.152030'),('vyefl9bkz3scunk9s9hw7rn6aoictc0f','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vquU8:Yc4Jyy_i08EA1XCnqrax9dvIAHoYExNLh72jt3ACIXM','2026-02-13 15:49:32.170678'),('vyswysko9e1iw3bsz47khr5qy6h7pceo','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1w7sCD:9unBMfqrNCSCz51LgEo31Iu7Vroq1UGkVaTMZtjbJE0','2026-04-01 10:49:09.558301'),('w0dj8yake5g4uh85zpary8qyc8gsl7lj','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vr9ZF:6_Xrvu1JEMwgfNKL19kXoDaXfJVWl1SkmvL1VZKvUKo','2026-02-14 07:55:49.624995'),('w2hncr29v995fiuv4fhmjh71gldxxofh','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1w4xca:ZiB_bIS_9Cb8fOkM9iWsnnhkxh_9s7MLq5Yn8nrsWsg','2026-03-24 10:00:20.000187'),('y8ex2kiw8ws3kjxocadyr13lgnnkmfuq','.eJw1y0sKgCAUQNG9vHGC-c_NiOYLhMxQgiLae0I0vBfODRlzwOqOI0WwMJrAZOSGRE09ESiR-EksxIigZ644U9HA8KNaVuzoq75dw9ZS2Ryee6oXWK4ofV4KlB9e:1vgKcs:RnT5mKlDM6lBRHtsQ8k5RivCCf2tUxF802OrhgoxXN0','2026-01-15 11:30:50.467611'),('ym5csixktglbq1t2ur48ftc8zn51kbj3','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vqqsh:c97WMD2KTQR5wm_gzwWJWYU6pRORE8p3ZVfzg4nPwLU','2026-02-13 11:58:39.673478'),('yn1fljnc2x7gmijrrmeyniwu1mjcb5yg','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1wAnGr:3AhXse8CjrvmYZ_j-DlI0VMuwC9s237ePre68G_mbZo','2026-04-09 12:10:01.914755'),('yu8tsq9pmy3dx2sqal7oobombnlswseb','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vr8QO:M3kjh5LkW_iwy7eadaX9WkXNboTV6RfXgBqbYIRMOME','2026-02-14 06:42:36.660320'),('z19m9n2um2jds83lkwxq33zyv51eds7g','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vduiJ:F3wBuCxO2nZ73K4SrbicPNMA6QoCRnpWxrReYUs2Wfo','2026-01-08 19:26:27.056008'),('zsy07hobj584y3nyv3mj3popux0aavn2','.eJwty0EKgCAQQNG7zDph1NLyMiI2wUBpKEIR3b2Ilv_DuyDMGyffGs_gwBor0dIiKAYlpFxQTMOkRcTeImk0o4rQ_abklV7zxTt9pVo5J0_HzuUEpw3i_QCCFB2i:1vfXOe:ddxn23HwPYcqeXQuE7dHAPSGwb-fzl9o1ovTxHg3U7c','2026-01-13 06:56:52.227299'),('zwz45upgc1l1hw5i7vgyrikt1f74hiie','.eJw1y0EKgCAQQNG7zLqByUzKO3QGURxByAwlKKK7J0HL_-HdkDg5LuY4ogcNs6deBGHRCyVQjsqhDZZQSs-TZclEBN2PSl65oeWrtk3lWmPeDJ97LBfoQRE9LxOjH3o:1vgfDx:OcGEF2Ch9Hsr4HfChRLbZUiOTztxTRigJp89aaV7_sM','2026-01-16 09:30:29.740316');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ig_account`
--

DROP TABLE IF EXISTS `ig_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ig_account` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uuid` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'admin' COMMENT 'admin | editor | viewer',
  `application_type` enum('observer','sig_member') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `application_status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'pending',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1=Active, 0=Disabled',
  `reset_token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reset_token_expires` bigint DEFAULT NULL,
  `otp` int DEFAULT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `failed_attempts` tinyint DEFAULT '0',
  `locked_until` timestamp NULL DEFAULT NULL,
  `member_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `member_grp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `designation` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sig_selection` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `linkedin` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ig_account`
--

LOCK TABLES `ig_account` WRITE;
/*!40000 ALTER TABLE `ig_account` DISABLE KEYS */;
INSERT INTO `ig_account` VALUES (1,'767107ef-eca2-11f0-9593-c0470e30682c','ig@nixi.in','pbkdf2_sha256$1000000$I1XdJJE9KAKYxh26c5zCiM$vc93W8BuVwjnDGyvuMWrVvjB9f0iG3ypAyIGHURkjHI=','admin',NULL,'pending',1,NULL,NULL,NULL,'2026-04-09 05:40:02','2026-01-08 14:58:16','2026-04-09 11:10:01',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'18b25d38-d70a-4e5e-a94f-84b7c36326d8','abhishek.suthar1@nixi.in','pbkdf2_sha256$1200000$EmjSqvfJnrtz8D0D1lW9pk$jAL4D3jIik+dhpRgEowAoy3vpMxUslq5pWwpbqn/BOM=','member',NULL,'pending',1,NULL,NULL,NULL,'2026-01-15 09:32:33','2026-01-09 00:36:49','2026-01-16 08:08:35',1,NULL,'IPS','SIG-1','Natational internet exchnage of india','8503013554',NULL,NULL,NULL,NULL,NULL),(5,'283d5f25-3753-4193-832c-b4d83a409acc','admin1@nixi.com','pbkdf2_sha256$1200000$EmjSqvfJnrtz8D0D1lW9pk$jAL4D3jIik+dhpRgEowAoy3vpMxUslq5pWwpbqn/BOM=','member',NULL,'pending',1,NULL,NULL,NULL,NULL,'2026-01-13 04:43:40','2026-01-14 11:15:10',0,NULL,'IPS','SIG-1','Natational internet exchnage of india','8503013554',NULL,NULL,NULL,NULL,NULL),(6,'d1bc9d33-5e1a-40ad-b663-3a3f4e3aa2cc','dhananjayk1@nsdl.com','pbkdf2_sha256$1200000$EmjSqvfJnrtz8D0D1lW9pk$jAL4D3jIik+dhpRgEowAoy3vpMxUslq5pWwpbqn/BOM=','member',NULL,'pending',1,NULL,NULL,NULL,NULL,'2026-01-13 04:54:29','2026-01-14 11:15:12',0,NULL,'IPS','SIG-1','Natational internet exchnage of india','9819092477',NULL,NULL,NULL,NULL,NULL),(7,'c0f22e38-15e0-4761-b78b-4f126afefd0b','abhishek33.suthar@nixi.in','pbkdf2_sha256$1200000$EmjSqvfJnrtz8D0D1lW9pk$jAL4D3jIik+dhpRgEowAoy3vpMxUslq5pWwpbqn/BOM=','member',NULL,'pending',1,NULL,NULL,NULL,NULL,'2026-01-13 04:59:41','2026-01-14 11:15:14',0,NULL,'IPS','SIG-1','national internet exchange of india','8503013554',NULL,NULL,NULL,NULL,NULL),(8,'a056b03b-0730-4501-99ba-14ae70553fd8','abhishek334.suthar@nixi.in','pbkdf2_sha256$1200000$EmjSqvfJnrtz8D0D1lW9pk$jAL4D3jIik+dhpRgEowAoy3vpMxUslq5pWwpbqn/BOM=','member',NULL,'pending',1,NULL,NULL,NULL,NULL,'2026-01-13 05:04:01','2026-01-14 11:15:28',0,NULL,'IPS','SIG-1','National internet exchnage of india','8503013554',NULL,NULL,NULL,NULL,NULL),(9,'dbbb0c3f-0f1b-4e51-ac35-5ec2b632e14c','abhisheksuthar01511@gmail.com','pbkdf2_sha256$1200000$qA1ggldF4qM6uUeQmnhwwW$IG6tkdhIqF3O/LmZa0MZD1ls0XHzPliTwrwkKBQesXk=','viewer',NULL,'pending',0,NULL,20260115092142,195415,NULL,'2026-01-15 09:11:41','2026-01-15 09:18:06',0,NULL,NULL,NULL,NULL,'8503013554',NULL,NULL,NULL,NULL,NULL),(10,'d12a68c5-bf3e-43c2-bd41-d236fcfb0241','abhisheksuthar0151@gmail.com','pbkdf2_sha256$1200000$oPrYN8W8uq3vrTz1iYGDG3$Gp60gOF94Sd65VKBV0/h+BCwv9ovMbK0kaU+/K1vQHg=','viewer',NULL,'pending',0,NULL,20260115092830,128863,NULL,'2026-01-15 09:18:30','2026-01-15 09:18:30',0,NULL,NULL,NULL,NULL,'8503013554',NULL,NULL,NULL,NULL,NULL),(11,'4a4ff23b-e36e-4425-b9aa-7aaa2d5eac1d','test@sify.com','pbkdf2_sha256$1200000$3IfJMhAYhdZbnLTBV8RLl8$0Sp/sjHKtWx3IWHbUwYzFRl+hNGa4p2rIwyddeTpvmY=','viewer',NULL,'pending',1,NULL,NULL,NULL,NULL,'2026-01-15 09:26:44','2026-01-15 09:29:56',0,NULL,NULL,NULL,NULL,'8503013554',NULL,NULL,NULL,NULL,NULL),(12,'9d012f2a-d262-456b-afa0-44de8ae4e000','test2@nixi.in','pbkdf2_sha256$1200000$agUVWL9pMKSFvu4TTHs20r$AkNiFM4vqdYN08tUqMbg0bFlzqpY6LUctxRuHChItzA=','Member',NULL,'pending',1,NULL,NULL,NULL,'2026-04-09 05:37:51','2026-01-15 09:31:08','2026-04-09 11:07:51',0,NULL,NULL,NULL,NULL,'8503013554',NULL,NULL,NULL,NULL,NULL),(13,'c1f9e2a1-8a3d-4c7e-9f11-123456789001','admin1@nixi.in','pbkdf2_sha256$1000000$HM9xVi9FoLM6rtOOL6Vya9$JVqp2wqAUTxE3g/19UZM5XQTOnyjaBe/XJ4BNoImwAk=','admin',NULL,'pending',1,NULL,NULL,NULL,'2026-02-06 10:41:52','2026-02-06 10:41:52','2026-03-04 04:44:28',0,NULL,'Core','Group-A','NIXI India','9876543210',NULL,NULL,NULL,NULL,NULL),(14,'c1f9e2a1-8a3d-4c7e-9f11-123456789002','editor1@nixi.in','pbkdf2_sha256$1200000$abc124xyz$asdlfkj234lkj23lkj4lkj23lkj4lkj23lk=','editor',NULL,'pending',1,NULL,NULL,NULL,'2026-02-06 10:41:52','2026-02-06 10:41:52','2026-02-06 10:41:52',0,NULL,'SIG','Group-B','Internet Society India','9123456780',NULL,NULL,NULL,NULL,NULL),(15,'c1f9e2a1-8a3d-4c7e-9f11-123456789003','viewer1@nixi.in','pbkdf2_sha256$1200000$abc125xyz$lkjsdf98u234lkj23lkj23lkj23lkj23lkj=','viewer',NULL,'pending',0,NULL,NULL,NULL,NULL,'2026-02-06 10:41:52','2026-02-06 10:41:52',0,NULL,'Observer','Group-C','Tech Policy Forum','9988776655',NULL,NULL,NULL,NULL,NULL),(16,'c1f9e2a1-8a3d-4c7e-9f11-123456789004','admin2@nixi.in','pbkdf2_sha256$1200000$abc126xyz$asdfasdlkfj234lkj23lkj23lkj23lkj23=','admin',NULL,'pending',0,NULL,NULL,NULL,'2026-02-06 10:41:52','2026-02-06 10:41:52','2026-02-06 10:41:52',0,NULL,'Core','Group-A','Digital Governance Council','9090909090',NULL,NULL,NULL,NULL,NULL),(17,'c1f9e2a1-8a3d-4c7e-9f11-123456789005','editor2@nixi.in','pbkdf2_sha256$1200000$abc127xyz$lkj23lkj23lkj23lkj23lkj23lkj23lkj2=','editor',NULL,'pending',1,NULL,NULL,NULL,'2026-02-06 10:41:52','2026-02-06 10:41:52','2026-02-06 10:41:52',0,NULL,'SIG','Group-D','Cyber Security Alliance','9012345678',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `ig_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ig_events`
--

DROP TABLE IF EXISTS `ig_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ig_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `event_link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `event_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ig_events`
--

LOCK TABLES `ig_events` WRITE;
/*!40000 ALTER TABLE `ig_events` DISABLE KEYS */;
INSERT INTO `ig_events` VALUES (26,'Lorem Ipsum is simply dummy text of','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop p','https://ix.nixi.in','events/1768478673_enevntimage.png','2026-01-29','2026-01-15 06:34:33','2026-02-12 11:20:12'),(31,NULL,'test description 4','https://ix.nixi.in','events/1768480552_enevntimage.png','2026-01-28','2026-01-15 07:05:53','2026-01-15 07:05:53'),(32,NULL,'test Descritipn','https://ix.nixi.in','events/1768480667_enevntimage.png','2026-01-29','2026-01-15 07:07:47','2026-01-15 07:07:47'),(33,NULL,'test description','https://test.com','events/1768480698_enevntimage.png','2026-01-26','2026-01-15 07:08:18','2026-01-15 07:08:18'),(34,'Lorem Ipsum is simply dummy text of','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop p','https://www.google.com/','events/1770914546_react-js-and-vite-js-logo-on-night-sky-background-3539552582.jpg','2026-02-19','2026-02-12 11:12:26','2026-02-12 11:19:47'),(35,'Test 001','Test 001','https://www.google.com/','events/1772601451_javascript.png','2026-03-12','2026-03-03 23:47:31','2026-03-03 23:47:31');
/*!40000 ALTER TABLE `ig_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ig_meetings`
--

DROP TABLE IF EXISTS `ig_meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ig_meetings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `meeting_date` date NOT NULL,
  `agenda_file` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `record_file` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `document_file` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('Upcoming','Completed','Deferred') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Upcoming',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ig_meetings`
--

LOCK TABLES `ig_meetings` WRITE;
/*!40000 ALTER TABLE `ig_meetings` DISABLE KEYS */;
INSERT INTO `ig_meetings` VALUES (1,NULL,'2026-01-09','meetings/agenda/1767898550_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/record/1767898550_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/document/1767898550_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','Upcoming','2026-01-08 18:55:50','2026-01-08 18:55:50'),(2,'askjdfkajskdflasdjf','2026-01-21','meetings/agenda/1767899521_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/record/1767899521_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/document/1767899521_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','Upcoming','2026-01-08 19:12:01','2026-01-08 19:12:01'),(3,'kjashdfkjahskjdfkasjkdfjaskdfjlaslkdfjlajsldfjalksdjflk','2026-01-21','meetings/agenda/1767899547_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/record/1767899547_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/document/1767899547_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','Upcoming','2026-01-08 19:12:27','2026-01-08 19:12:27'),(4,'.jksdhfkjasdkfjaksdjfkjasjdflnalksd f;lanscd','2026-01-22','meetings/agenda/1767899569_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/record/1767899569_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','meetings/document/1767899569_Fwd_ DNS & TXT Record Details for Domain Configuration.pdf','Upcoming','2026-01-08 19:12:50','2026-01-08 19:12:50');
/*!40000 ALTER TABLE `ig_meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interns_zone`
--

DROP TABLE IF EXISTS `interns_zone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interns_zone` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `college` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `specialization` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Biography` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Testimonial` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Project` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `upload_path` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creation_timestamp` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interns_zone`
--

LOCK TABLES `interns_zone` WRITE;
/*!40000 ALTER TABLE `interns_zone` DISABLE KEYS */;
/*!40000 ALTER TABLE `interns_zone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stakeholder_consultations`
--

DROP TABLE IF EXISTS `stakeholder_consultations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stakeholder_consultations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `open_date` date DEFAULT NULL,
  `close_date` date DEFAULT NULL,
  `organization` enum('NIXI','MeitY','Other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `input_focus` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `proposals` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `contact_email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requester` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('Draft','Open','Closed','Archived') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Draft',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stakeholder_consultations`
--

LOCK TABLES `stakeholder_consultations` WRITE;
/*!40000 ALTER TABLE `stakeholder_consultations` DISABLE KEYS */;
INSERT INTO `stakeholder_consultations` VALUES (1,'Test title','Test descriptipn',NULL,NULL,'NIXI',NULL,NULL,NULL,NULL,NULL,'Open','2026-01-12 16:24:03','2026-01-12 16:24:03'),(3,'Proposed GNSO Process for ICANN Board to Reverse Adoption of GNSO Policy Recommendations','This proceeding seeks community input on a proposed process that would allow the ICANN Board to reverse adoption of GNSO policy recommendations under defined circumstances.','2026-01-13','2026-01-28','NIXI',NULL,NULL,NULL,'Policy',NULL,'Open','2026-01-13 07:22:04','2026-01-13 07:22:04'),(4,'asdfasdf','asdfasdfasdf','2026-01-21','2026-01-27','NIXI','asdfasdfasdf','','','Policy','','Open','2026-01-13 07:32:03','2026-01-13 07:32:03'),(5,'String Similarity Evaluation Guidelines for New gTLD Program: 2026 Round','String Similarity Evaluation (SSE) will be a part of the New gTLD Program: 2026 Round application process. SSE prevents user confusion resulting from the delegation of visually similar strings. ICANN developed guidelines for an SSE panel to conduct an evaluation using the pre-screening report generated by the SSE tool and related SSE data.','2026-01-13','2026-01-15','NIXI','ICANN org has updated the String Similarity Evaluation (SSE) Guidelines, which are intended to be used by the SSE panel, along with the SSE tool and related SSE data (published for public comment), to conduct an evaluation of the applied-for strings in the New gTLD Program: 2026 Round. SSE prevents user confusion resulting from the delegation of visually similar strings. These guidelines are being published for community input.\r\n\r\n\r\n','','','Technical','','Open','2026-01-13 07:57:16','2026-01-13 07:57:16'),(6,'Lorem Ipsum','Lorem Ipsum','2026-03-10','2026-03-20','NIXI','Lorem Ipsum','Lorem Ipsum','jainvaibhav415@gmail.com','Regulation','vaibhav.buccha@gmail.com','Open','2026-03-06 08:09:09','2026-03-06 08:09:09'),(7,'Lorem Ipsum is simply dummy text of the printing and typesetting industry.','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum','2026-03-23','2026-03-28','NIXI','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum','Test@nixi.in','Regulation','Test@nixi.in','Open','2026-03-24 08:59:47','2026-03-24 08:59:47');
/*!40000 ALTER TABLE `stakeholder_consultations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stakeholder_documents`
--

DROP TABLE IF EXISTS `stakeholder_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stakeholder_documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `consultation_id` int NOT NULL,
  `document_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `document_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `document_type` enum('pdf','doc','docx') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `consultation_id` (`consultation_id`),
  CONSTRAINT `stakeholder_documents_ibfk_1` FOREIGN KEY (`consultation_id`) REFERENCES `stakeholder_consultations` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stakeholder_documents`
--

LOCK TABLES `stakeholder_documents` WRITE;
/*!40000 ALTER TABLE `stakeholder_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `stakeholder_documents` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-24 20:25:36

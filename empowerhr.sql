-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 11, 2023 at 03:29 AM
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
-- Database: `empowerhr`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkcomplaint` (`$complaintid` INT)   BEGIN
	declare results int;
	select count(*) into results from complaints where complaintid=$complaintid;
	
	-- displays 1 if complaint exists and 0 otherwise
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkdepartment` (`$departmentid` INT)   BEGIN
	declare results int;
	select count(*) into results from department where departmentid=$departmentid;
	
	-- displays 1 if department exists and 0 if it doesnt exist
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkemployee` (`$employeeid` INT)   BEGIN
	declare results int;
	select count(*) into results from employee where employeeid = $employeeid;
	-- diplays 1 if employee exists and 0 if employee doesn't exist
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkleaverequest` (`$leaverequestid` INT)   BEGIN
	declare results int;
	select count(*) into results from leaverequest where leaverequestid=$leaverequestid;
	
	-- displays 1 if leaverequest exists and 0 otherwise
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkrole` (`$roleid` INT)   BEGIN
	declare results int;
	select count(*) into results from `role` where roleid=$roleid;
	
	-- displays 1 if role already exists and 0 if otherwise
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checksuggestion` (`$suggestionid` INT)   BEGIN
	declare results int;
	select count(*) into results from suggestions where suggestionid=$suggestionid;
	
	-- displays 1 if suggestion exists and 0 otherwise
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_checkuser` (`$userid` INT)   BEGIN
	declare results int;
	select count(*) into results from users where userid=$userid;
	
	-- displays 1 if user exists and 0 otherwise
	select results;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deletecomplaint` (`$complaintid` INT)   BEGIN
		update complaints
		set deleted = 1,datedeleted=now()
		where complaintid=$complaintid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deletedepartment` (`$departmentid` INT)   BEGIN
		update department
		set deleted=1,datedeleted=now()
		where departmentid=$departmentid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteemployee` (`$employeeid` INT)   BEGIN
		update employee
		set deleted = 1
		where employeeid=$employeeid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteleaverequest` (`$leaverequestid` INT)   BEGIN
	update leaverequest
	set deleted=1,datedeleted=now()
	where leaverequestid=$leaverequestid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deletenotification` (`$notificationid` INT)   BEGIN
	update notifications
	set deleted=1,datedeleted=now()
	where notificationid=$notificationid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleterole` (`$roleid` INT)   BEGIN
		update `role`
		set deleted=1,datedeleted=now()
		where roleid=$roleid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deletesuggestion` (`$suggestionid` INT)   BEGIN
		update suggestions
		set deleted=1,datedeleted=now()
		where suggestionid=$suggestionid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteuser` (`$userid` INT)   BEGIN
	update users
	set deleted=1,datedeleted=now()
	where userid=$userid;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getcomplaints` ()   BEGIN
	select * from complaints where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getdepartments` ()   BEGIN
	select * from department where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getemployee` ()   BEGIN
	select * from employee where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getleaverequests` ()   BEGIN
	select * from leaverequest where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getroles` ()   BEGIN
	select * from `role` where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getsuggestions` ()   BEGIN
	select * from suggestions where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getusers` ()   BEGIN
	select * from users where deleted=0;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_savecomplaint` (`$complaintid` INT, `$employeeid` INT, `$complainttype` VARCHAR(50), `$complaintdescription` VARCHAR(1000), `$complaintstatus` VARCHAR(50))   BEGIN
	declare complaint_exists int;
	select count(*) into complaint_exists from complaints where complaintid=$complaintid;
	
	if complaint_exists=0 then
		insert into  complaints(complaintid,employeeid,`type`,`description`,`status`)
		values($complaintid,$employeeid,$complainttype,$complaintdescription,$complaintstatus);
	else
		update complaints
		set employeeid=$employeeid,`type`=complainttype,`description`=complaintdescription,`status`=complaintstatus
		where complaintid=4complaintid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_savedepartment` (`$departmentid` INT, `$departmentname` VARCHAR(50))   BEGIN
	declare department_exists int;
	select count(*) into department_exists from department where departmentid=$departmentid;
	
	if department_exists=0 then
		insert into department(departmentid,departmentname)
		values($departmentid,$departmentname);
	else
		update department
		set departmentname=$departmentname
		where departmentid=$departmentid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_saveemployee` (`$employeeid` INT, `$firstname` VARCHAR(50), `$lastname` VARCHAR(50), `$email` VARCHAR(50), `$dateofbirth` DATE, `$phonenumber` VARCHAR(50), `$address` VARCHAR(50), `$hiredate` DATETIME, `$departmentid` INT, `$roleid` INT)   BEGIN
	declare employee_exists int;
	select count(*) into employee_exists from employee where employeeid = $employeeid;
	
	if employee_exists=0 then
		insert into employee(employeeid,firstname,lastname,email,dateofbirth,phonenumber,address,hiredate,departmentid,roleid)
		values($employeeid,$firstname,$lastname,$email,$dateofbirth,$phonenumber,$address,$hiredate,$departmentid,$roleid);
	else
		update employee
		set firstname=$firstname,lastname=$lastname,email=$email,dateofbirth=$dateofbirth,address=$address,hiredate=$hiredate,departmentid=$departmentid,roleid=$roleid
		where employeeid = $employeeid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_saveleaverequest` (`$leaverequestid` INT, `$employeeid` INT, `$leavetype` VARCHAR(50), `$startdate` DATE, `$enddate` DATE, `$leaverequeststatus` VARCHAR(50), `$reason` VARCHAR(1000))   BEGIN
	declare leaverequest_exists int;
	select count(*) into leaverequest_exists from leaverequest where leaverequestid=$leaverequestid;
	
	if leaverequest_exists=0 then
		insert into leaverequest(leaverequestid,employeeid,leavetype,startdate,enddate,`status`,reason)
		values($leaverequestid,$employeeid,$leavetype,$startdate,$enddate,$leaverequeststatus,$reason);
	else
		update leaverequest
		set employeeid=$employeeid,leavetype=$leavetype,startdate=$startdate,enddate=$enddate,`status`=$leaverequeststatus,reason=$reason
		where leaverequestid=$leaverequestid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_savenotification` (`$notificationid` INT, `$employeeid` INT, `$notificationtype` VARCHAR(50), `$message` VARCHAR(1000))   BEGIN
	insert into notifications(notificationid,employeeid,notificationtype,message)
	values($notificationid,$employeeid,$notificationtype,$message);
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_saverole` (`$roleid` INT, `$rolename` VARCHAR(50))   BEGIN
	declare role_exists int;
	select count(*) into role_exists from `role` where roleid=$roleid;
	
	if role_exists=0 then
		insert into `role`(roleid,rolename)
		values($roleid,$rolename);
	else
		update `role`
		set rolename=$rolename
		where roleid=$roleid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_savesuggestion` (`$suggestionid` INT, `$employeeid` INT, `$suggestiondescription` VARCHAR(1000), `$suggestionstatus` VARCHAR(50))   BEGIN
	declare suggestion_exists int;
	select count(*) into suggestion_exists from suggestions where suggestionid=$suggestionid;
	
	if suggestion_exists = 0 then
		insert into suggestions(suggestionid,employeeid,`description`,`status`)
		values($suggestionid,$employeeid,$suggestiondescription,$suggestionstatus);
	else
		update suggestions
		set employeeid=$employeeid,`descriptionn`=$suggestiondescription,`status`=$suggestionstatus
		where suggestionid=$suggestionid;
	end if;
	END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_saveuser` (`$userid` INT, `$employeeid` INT, `$username` VARCHAR(50), `$passwordhash` VARCHAR(50))   BEGIN
	declare user_exists int;
	select count(*) into user_exists from users where userid=$userid;
	
	if user_exists = 0 then
		insert into users(userid,employeeid,username,passwordhash)
		values($userid,$employeeid,$username,$passwordhash);
	else
		update users
		set employeeid=$employeeid,username=$username,passwordhash=$passwordhash
		where userid=$userid;
	end if;
	END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `complaints`
--

CREATE TABLE `complaints` (
  `complaintid` int(11) NOT NULL,
  `employeeid` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `dateadded` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `dapartmentid` int(11) NOT NULL,
  `departmentname` varchar(50) DEFAULT NULL,
  `dateadded` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `employeeid` int(11) NOT NULL,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `dateofbirth` date DEFAULT NULL,
  `phonenumber` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `hiredate` timestamp NOT NULL DEFAULT current_timestamp(),
  `departmentid` int(11) DEFAULT NULL,
  `roleid` int(11) DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leaverequest`
--

CREATE TABLE `leaverequest` (
  `leaverequestid` int(11) NOT NULL,
  `employeeid` int(11) DEFAULT NULL,
  `leavetype` varchar(50) DEFAULT NULL,
  `startdate` date DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `reason` varchar(1000) DEFAULT NULL,
  `dateadded` timestamp NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notificationid` int(11) NOT NULL,
  `employeeid` int(11) DEFAULT NULL,
  `notificationtype` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `message` varchar(1000) DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `roleid` int(11) NOT NULL,
  `rolename` varchar(50) DEFAULT NULL,
  `dateadded` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `suggestions`
--

CREATE TABLE `suggestions` (
  `suggestionid` int(11) NOT NULL,
  `employeeid` int(11) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `dateadded` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `employeeid` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `passwordhash` varchar(50) DEFAULT NULL,
  `dateadded` timestamp NOT NULL DEFAULT current_timestamp(),
  `deleted` tinyint(1) DEFAULT 0,
  `datedeleted` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userid`, `employeeid`, `username`, `passwordhash`, `dateadded`, `deleted`, `datedeleted`) VALUES
(1, 1, 'admin', 'admin', '2023-12-11 02:23:22', 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `complaints`
--
ALTER TABLE `complaints`
  ADD PRIMARY KEY (`complaintid`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`dapartmentid`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`employeeid`);

--
-- Indexes for table `leaverequest`
--
ALTER TABLE `leaverequest`
  ADD PRIMARY KEY (`leaverequestid`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notificationid`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`roleid`);

--
-- Indexes for table `suggestions`
--
ALTER TABLE `suggestions`
  ADD PRIMARY KEY (`suggestionid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `complaints`
--
ALTER TABLE `complaints`
  MODIFY `complaintid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `dapartmentid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `employeeid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `leaverequest`
--
ALTER TABLE `leaverequest`
  MODIFY `leaverequestid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notificationid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `roleid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `suggestions`
--
ALTER TABLE `suggestions`
  MODIFY `suggestionid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

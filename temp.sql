DELETE FROM medicalManagerWeb_usersignuprequest;
DELETE FROM medicalManagerWeb_medicaluser;
DELETE FROM medicalManagerWeb_doctor;
DELETE FROM medicalManagerWeb_keytoken;
DELETE FROM medicalManagerWeb_role;
DELETE FROM medicalManagerWeb_record;
DELETE FROM medicalManagerWeb_template;
DELETE FROM medicalManagerWeb_treatment;
DELETE FROM medicalManagerWeb_patient;
DROP TABLE medicalManagerWeb_record;

DELETE FROM medicalManagerWeb_doctor WHERE id='a208e9d416a345828710718997436e22';


UPDATE medicalManagerWeb_doctor
SET user_id = "bbfbefd6413f49049861a6ca27b6ffbe"
WHERE id="667c5520dad94a41a9e09c75301bb519"	
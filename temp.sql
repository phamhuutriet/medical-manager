DELETE FROM medicalManagerWeb_usersignuprequest;
DELETE FROM medicalManagerWeb_medicaluser;
DELETE FROM medicalManagerWeb_doctor;
DELETE FROM medicalManagerWeb_keytoken;
DELETE FROM medicalManagerWeb_role;
DELETE FROM medicalManagerWeb_record;
DELETE FROM medicalManagerWeb_template;
DELETE FROM medicalManagerWeb_treatment;
DROP TABLE medicalManagerWeb_record;

DELETE FROM medicalManagerWeb_doctor WHERE id='a208e9d416a345828710718997436e22';
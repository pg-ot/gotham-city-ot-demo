connect 'jdbc:derby:/opt/tomcat/webapps/ScadaBR/db/scadabrDB';
UPDATE users SET password = 'admin';
SELECT id, username, password FROM users;
disconnect;
exit;

connect 'jdbc:derby:/opt/tomcat/webapps/ScadaBR/db/scadabrDB';
SELECT id, username, password FROM users;
disconnect;
exit;

connect 'jdbc:derby:/opt/tomcat/webapps/ScadaBR/db/scadabrDB';
UPDATE users SET password = '0DPiKuNIrrVmD8IUCuw1hQxNqZc=';
SELECT id, username, password FROM users;
disconnect;
exit;

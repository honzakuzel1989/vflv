ALTER TABLE users ADD COLUMN nickname TEXT default '';

UPDATE users SET nickname = 'Honza' WHERE name = 'kuz1';
UPDATE users SET nickname = 'Luboš' WHERE name = 'kli1';
UPDATE users SET nickname = 'Marťas' WHERE name = 'mar5';
UPDATE users SET nickname = 'Petr' WHERE name = 'kor1';
UPDATE users SET nickname = 'Ondra' WHERE name = 'dyc1';
UPDATE users SET nickname = 'Tomáš' WHERE name = 'flo2';
UPDATE users SET nickname = 'Standa' WHERE name = 'bel1';
UPDATE users SET nickname = 'Michal' WHERE name = 'kre2';
UPDATE users SET nickname = 'Zdéňa' WHERE name = 'cvr1';
UPDATE users SET nickname = 'Eva' WHERE name = 'tes2';
UPDATE users SET nickname = 'Ruda' WHERE name = 'buc1';
UPDATE users SET nickname = 'Adam' WHERE name = 'tom3';
UPDATE users SET nickname = 'Lukáš' WHERE name = 'bud1';

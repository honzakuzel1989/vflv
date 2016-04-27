ALTER TABLE pubs ADD COLUMN visible INTEGER default 1;
ALTER TABLE pubs ADD COLUMN url TEXT default 'http://obed.cvrkal.cz/nabidka-dne/';

UPDATE pubs SET visible = 0 WHERE title = 'Zakki';

UPDATE pubs SET url = 'http://pizzazz.cz/poledni-menu/' WHERE title = 'Pizzaz';
UPDATE pubs SET url = 'https://www.facebook.com/pizzerielysice/' WHERE title = 'Emanuel';

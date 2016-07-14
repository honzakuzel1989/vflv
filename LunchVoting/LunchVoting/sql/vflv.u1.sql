ALTER TABLE pubs ADD COLUMN visible INTEGER default 1;
ALTER TABLE pubs ADD COLUMN url TEXT default 'http://obed.cvrkal.cz/nabidka-dne/';

UPDATE pubs SET visible = 0 WHERE title = 'Zakki';
UPDATE pubs SET visible = 0 WHERE title = 'Kruháč';

UPDATE pubs SET url = 'http://pizzazz.cz/poledni-menu/' WHERE title = 'Pizzaz';
UPDATE pubs SET url = 'https://www.facebook.com/pizzerielysice/' WHERE title = 'Emanuel';
UPDATE pubs SET url = 'http://www.hradekrajecko.cz/index.php/tydenni-menu' WHERE title = 'Hrádek';
UPDATE pubs SET url = 'http://www.sypkablansko.cz/cz/restaurace/denni-menu' WHERE title = 'Sýpka';
UPDATE pubs SET url = 'https://www.facebook.com/hotelsladovna' WHERE title = 'Sladovna';
UPDATE pubs SET url = 'http://www.pizzerie-piccolo.cz/cerna-hora/denni-menu' WHERE title = 'Picolo';
UPDATE pubs SET url = 'https://www.facebook.com/LidovyDumLysice' WHERE title = 'Liďák';
UPDATE pubs SET url = 'http://www.kopecek.cz/denni-menu' WHERE title = 'Kopec';
UPDATE pubs SET url = 'http://www.ebdiners.cz/#!t-denn--menu/ciho' WHERE title = 'EB';
UPDATE pubs SET url = 'https://www.menicka.cz/1275-restaurace-aquapark.html' WHERE title = 'Aqua';

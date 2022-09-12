// CREATE INDEX ON :Category(catId);

// CREATE INDEX ON :Category(catName);

// CREATE INDEX ON :Page(pageTitle);

// CREATE (c:Category:RootCategory {catId: 0, catName: 'Databases', subcatsFetched : false, pagesFetched : false, level: 0 });

UNWIND range(0,3) as level
CALL apoc.cypher.doIt("
MATCH (c:Category { subcatsFetched: false, level: $level})
CALL apoc.load.json('https://en.wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:' + apoc.text.urlencode(c.catName) + '&cmprop=ids%7Ctitle&cmlimit=500')
YIELD value as results
UNWIND results.query.categorymembers AS subcat
MERGE (sc:Category {catId: subcat.pageid})
ON CREATE SET sc.catName = substring(subcat.title,9),
              sc.subcatsFetched = false,
              sc.pagesFetched = false,
              sc.level = $level + 1
WITH sc,c
CALL apoc.create.addLabels(sc,['Level' +  ($level + 1) + 'Category']) YIELD node
MERGE (sc)-[:SUBCAT_OF]->(c)
WITH DISTINCT c
SET c.subcatsFetched = true", { level: level }) YIELD value
RETURN value;


UNWIND range(0,4) as level
CALL apoc.cypher.doIt("
MATCH (c:Category { pagesFetched: false, level: $level })
CALL apoc.load.json('https://en.wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmtype=page&cmtitle=Category:' + apoc.text.urlencode(c.catName) + '&cmprop=ids%7Ctitle&cmlimit=500')
YIELD value as results
UNWIND results.query.categorymembers AS page
MERGE (p:Page {pageId: page.pageid})
ON CREATE SET p.pageTitle = page.title, p.pageUrl = 'http://en.wikipedia.org/wiki/' + apoc.text.urlencode(replace(page.title, ' ', '_'))
WITH p,c
MERGE (p)-[:IN_CATEGORY]->(c)
WITH DISTINCT c
SET c.pagesFetched = true", { level: level }) yield value
return value
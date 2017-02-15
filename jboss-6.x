/server/all/data
/server/all/log
/server/all/tmp
/server/all/work
/server/default/data
/server/default/log
/server/default/tmp
/server/default/work
/server/minimal/data
/server/minimal/log
/server/minimal/tmp
/server/minimal/work
/server/jbossweb-standalone/data
/server/jbossweb-standalone/log
/server/jbossweb-standalone/tmp
/server/jbossweb-standalone/work
/server/standard/data
/server/standard/log
/server/standard/tmp
/server/standard/work 
/server/default/deploy/*.jar.failed
/server/default/deploy/*.jar.dodeploy
/server/default/deploy/*.xml.failed
/server/default/deploy/*.xml.dodeploy
/server/default/deploy/*.war.failed
/server/default/deploy/*.war.dodeploy

/*
*Important
* Case your directory for example
* /server/minimal/lib be empty. 
* The git will not submit this directory for you repository.
* In this case is necessary create one archive, for example .gitignore empty in this directory.
* Case you run your server without this directory the server will faild when you start service.
*/


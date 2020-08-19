var express = require('express');
var router = express.Router();
let {PythonShell} = require('python-shell')


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Options Analysis Service' });
});

/* GET home page. */
router.get('/sellputs', function(req, res, next) {
  let tickerList = req.query.tickers
  let investment = req.query.investment

  console.log("Processing request ", tickerList, investment);

  let cwd = process.cwd();
  let script = cwd + "../../download.py";

  PythonShell.run(script, {'args': [tickerList, investment, "none", "-o"]},
      function (err, results) {
                if (err)
                  throw err;
                res.send(results)
                console.log('finished');
              });


  // let spawn = require("child_process").spawn;
  // let process = spawn('python', ["../../download.py",
  //   tickerList,
  //   investment,
  //   "-o"]);
  // process.stdout.on('data', function (data) {
  //   console.log("WRITE DATA")
  //   res.write(data.toString());
  //   res.end('end')
  // })
  //
  //
  // process.stderr.on('data', (data) => {
  //   console.log(`stderr: ${data}`);
  // });
  //
  // process.on('close', (code) => {
  //   console.log(`child process exited with code ${code}`);
  // });
});


module.exports = router;

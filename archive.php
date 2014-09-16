<?php include 'head.html' ?>
<body onload="prettyPrint()">
  <div id="wrapper">
	<div id = "header">
	<br/>
	<div id="logo">
	  <h1><a>Machine Learning Club</a></h1>
	  <span class="slogan">University of Victoria</span> 
	</div>
  </div>
<?php $tab = substr($_SERVER['PHP_SELF'],9); include 'menu.php'; ?>
<div id = "page">
  <div id ="content">
	<div class = "box">
	<p>   
	<h3>previous talks and tutorials</h3>
	<a href="ml_meetings_intro.pdf">ML introduction slides</a> <br>
	Introduction slides about the club and machine learning. 
	<hr>
	<a href="Titanic_challenge.pdf">Titanic challenge slides</a><br>
	Slides on the Kaggle Titanic challenge. Starter code can be found <a href="mymodel.py">here</a>
	<hr>
	<a href="ml_club_higgs.pdf">Kaggle Higgs challenge slides</a><br>
	Slides about the Kaggle Higgs challenge. The starter code can be found <a href="higgs_model_py.py">here</a>
	<hr>
	<a href="NN_programming_club.pdf">Neural Networks and Deep Learning</a>
	<br>
	James' talk on Neural Networks and deep learning. 
	</p>
	</div>
  </div> 
</div>
</body>
</html>

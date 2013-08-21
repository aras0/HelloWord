
/*The mouseleave event occurs when the mouse pointer leaves the selected element
The mouseenter event occurs when the mouse pointer is over (enters) the selected element
*/
$(document).ready(function (){
    $('ul.menu li').mouseenter(function(){
        $(this).children('ul').slideDown('fast');
    });

    $('ul.menu li').mouseleave(function(){
        $(this).children('ul').slideUp('fast');
    });

});


/*mouseover i mouseout - kursor znalazł się i zszedł z obszaru*/
/*
$(document).ready(function (){
    $('ul.menu li').mouseover(function(){
        $(this).children('ul').slideDown('fast');
    });

    $('ul.menu li').mouseout(function(){
        $(this).children('ul').slideUp('fast');
    });

});
*/


/*Po najechaniu kursorem na dane pole menu skrypt sprawdza czy posiada on zagnieżdżoną listę 
(czyli czy do danego pola menu jest przypisane pod menu). Jeśli tak rozwija je. 
Po opuszczeniu przez kursor pola danego menu, pod menu jest zwijane, jeśli takowe istniało oczywiście.*/


/*
			var strony = document.getElementsByClassName('p');

			console.log(strony[1]); //to nie jest istotne w strukturze strony, ale pomaga przy sprawdzaniu projektowanych funkcjonalności
			for (var i in strony)
			{
				console.log(strony[i]);
			}
			*/
			
			
			
			
			

function ukryj(d)
{
  if (d.length < 1)
    return;

  document.getElementById(d).style.display = "none";
}

function pokaz(d,e)
{
  if (d.length < 1)
    return;
  document.getElementById(d).style.display = "block";

}

var divy = ["p11", "p12", "p13", "p41", "p42", "p121"];

function pokazUkryj(d)
{
	for(var i=0; i<window.divy.length; i++)
	{
	var obiekt = document.getElementById(window.divy[i]);
				if (obiekt.style.display == 'block') {
				obiekt.style.display = 'none';
				} else {
				obiekt.style.display = 'none';
				}
	}
document.getElementById(d).style.display = "block";
}




function ukrywaj(d,e,f,g,h)
{

  document.getElementById(d).style.display = "none";
  document.getElementById(e).style.display = "none";
  document.getElementById(f).style.display = "none";
  document.getElementById(g).style.display = "none";
  document.getElementById(h).style.display = "none";

}



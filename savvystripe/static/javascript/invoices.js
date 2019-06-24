$(document).ready(function(){

$( "td.date" ).each(function( i ) {
   var utcSeconds = parseInt($( this ).text(),10);
   var d = new Date(utcSeconds*1000);
   d.toISOString();
   $(this).html("<td class='date'>" + d + "</td>")});
});
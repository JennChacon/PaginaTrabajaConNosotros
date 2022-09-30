
$('i#prev').click(function() {
    $('.slider').slider('prev');
});

$('i#next').click(function() {
    $('.slider').slider('next');
});

$('.slider').slider({
    fullWidth: true,
    indicators: false,
    interval: 2000,
});



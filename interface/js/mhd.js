var current_elements = {images:[], sounds:[]}
make_embed_sound = function(sound) {
    return "<div class=\"sound\" " + "id=\"" + sound.id + "\">" +
        "<img width=\"32\" class=\"invisible\" src=\"/interface/images/thumbsup-small.png\" onclick=\"click_element('s', " +sound.id + ")\" />" +
           "<iframe frameborder=\"0\" scrolling=\"no\" src=\"" +
           sound.embed_url + "\" width=\"481\" height=\"86\"></iframe></div>";
};

make_embed_image = function(image, index) {
    return "<div class=\"photo\" id=" + image.id + ">" +
        "<img width=\"100%\" class=\"size" + index + "\" src=\"" + image.embed_url + "\""+
        "onclick=\"click_element('p', " + image.id + ")\"/> </div>";
}

var click_element = function(type, target) {
    $("#progressbar").progressbar("option", "value", 0);
    console.log("getting more things like  " +  target);
    var current_ids = {images: [], sounds: []};

    $.each(current_elements.images, function(index, image) {
        current_ids.images.push(image.id);
    });

    $.each(current_elements.sounds, function(index, sound) {
        current_ids.sounds.push(sound.id);
    });

    $.ajax({
        settings: {
            contentType: "application/json",
            },
            url:"http://localhost:5000/" + type + '/' + target,
        type: "POST",
        data: JSON.stringify(current_ids),
        success: build_gui,
        fail: function() { console.log("error getting more sounds and images") }
    });
};

function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

var build_gui = function(data) {
    console.log(data);
    current_elements = data;

    shuffled_images = shuffle(data.images.slice(0, 10));
    console.log(shuffled_images);
    $("#photo_container").empty();
    $.each(shuffled_images, function(index, element) {
        if (index < 10) {
            $("#photo_container").append(make_embed_image(element, element.rank));
        }
    });

    var wall = new freewall("#photo_container");
    wall.reset({
        selector: '.photo',
        animate: true,
        cellW: 160,
        cellH: 'auto',
        onResize: function() {
            wall.fitWidth();
        }
    });

    var images = wall.container.find('.photo');
    images.find('img').load(function() {
        wall.fitWidth();
    });


    $("#sound_container").empty();
    $.each(data.sounds, function(index, element) {
        if (index < 10) {
            $("#sound_container").append(make_embed_sound(element));
        }
    });
    if ($("#progressbar").progressbar("option", "value") < 90) {
        $("#progressbar").progressbar("option", "value", 95);
    }
};

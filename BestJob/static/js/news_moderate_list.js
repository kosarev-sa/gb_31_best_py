const newsTitleEls = $(".news-title");
const preBrowse = $(".pre-browse-panel");
const maxPreBrowseLen = 1000;
const browseHideButton = $(".btn-browse-hide");
const newsTextPanel = $(".browse-news");
newsTextPanel.hide()
preBrowse.hide();


function getNewsText(title_el) {
    return $(title_el).parents(".card-body").find(".news-body").html();
}

newsTitleEls.click(function () {
    let newsText = getNewsText(this);
    let browseNewsText = $(".browse-news-text");

    browseNewsText.text(newsText);
    newsTextPanel.show();
});

newsTitleEls.hover(
    function () {
        let newsText = getNewsText(this);
        if (newsText.length > maxPreBrowseLen) {
            console.log("more");
            console.log(newsText);
            let slicedText = newsText.slice(0 ,maxPreBrowseLen) + " ...";
            newsText = slicedText;
        }
        $(".docked-prebrowse-text").text(newsText);
        preBrowse.show();
    },
    function () {
    preBrowse.hide();
    }
);

browseHideButton.click(function () {
    newsTextPanel.hide();
});

for ( el of $(".is_active_text")) {
    if ($(el).text() == "Да") {
        $(el).addClass("text-success");
    } else {
        $(el).addClass("text-danger");
    }
}

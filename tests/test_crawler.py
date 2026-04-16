import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, Mock

from src.crawler import crawlQuotes, crawlAuthors, crawl


# =========================================================
# MOCK HTML (matches quotes.toscrape.com structure)
# =========================================================

QUOTE_PAGE_HTML = """
<html lang="en"><head>
	<meta charset="UTF-8">
	<title>Quotes to Scrape</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
    <link rel="stylesheet" href="/static/main.css">
    
    
</head>
<body>
    <div class="container">
        <div class="row header-box">
            <div class="col-md-8">
                <h1>
                    <a href="/" style="text-decoration: none">Quotes to Scrape</a>
                </h1>
            </div>
            <div class="col-md-4">
                <p>
                
                    <a href="/login">Login</a>
                
                </p>
            </div>
        </div>
    

<div class="row">
    <div class="col-md-8">

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="change,deep-thoughts,thinking,world"> 
            
            <a class="tag" href="/tag/change/page/1/">change</a>
            
            <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
            
            <a class="tag" href="/tag/thinking/page/1/">thinking</a>
            
            <a class="tag" href="/tag/world/page/1/">world</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“It is our choices, Harry, that show what we truly are, far more than our abilities.”</span>
        <span>by <small class="author" itemprop="author">J.K. Rowling</small>
        <a href="/author/J-K-Rowling">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="abilities,choices"> 
            
            <a class="tag" href="/tag/abilities/page/1/">abilities</a>
            
            <a class="tag" href="/tag/choices/page/1/">choices</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="inspirational,life,live,miracle,miracles"> 
            
            <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>
            
            <a class="tag" href="/tag/life/page/1/">life</a>
            
            <a class="tag" href="/tag/live/page/1/">live</a>
            
            <a class="tag" href="/tag/miracle/page/1/">miracle</a>
            
            <a class="tag" href="/tag/miracles/page/1/">miracles</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”</span>
        <span>by <small class="author" itemprop="author">Jane Austen</small>
        <a href="/author/Jane-Austen">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="aliteracy,books,classic,humor"> 
            
            <a class="tag" href="/tag/aliteracy/page/1/">aliteracy</a>
            
            <a class="tag" href="/tag/books/page/1/">books</a>
            
            <a class="tag" href="/tag/classic/page/1/">classic</a>
            
            <a class="tag" href="/tag/humor/page/1/">humor</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”</span>
        <span>by <small class="author" itemprop="author">Marilyn Monroe</small>
        <a href="/author/Marilyn-Monroe">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="be-yourself,inspirational"> 
            
            <a class="tag" href="/tag/be-yourself/page/1/">be-yourself</a>
            
            <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“Try not to become a man of success. Rather become a man of value.”</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="adulthood,success,value"> 
            
            <a class="tag" href="/tag/adulthood/page/1/">adulthood</a>
            
            <a class="tag" href="/tag/success/page/1/">success</a>
            
            <a class="tag" href="/tag/value/page/1/">value</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“It is better to be hated for what you are than to be loved for what you are not.”</span>
        <span>by <small class="author" itemprop="author">André Gide</small>
        <a href="/author/Andre-Gide">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="life,love"> 
            
            <a class="tag" href="/tag/life/page/1/">life</a>
            
            <a class="tag" href="/tag/love/page/1/">love</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“I have not failed. I've just found 10,000 ways that won't work.”</span>
        <span>by <small class="author" itemprop="author">Thomas A. Edison</small>
        <a href="/author/Thomas-A-Edison">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="edison,failure,inspirational,paraphrased"> 
            
            <a class="tag" href="/tag/edison/page/1/">edison</a>
            
            <a class="tag" href="/tag/failure/page/1/">failure</a>
            
            <a class="tag" href="/tag/inspirational/page/1/">inspirational</a>
            
            <a class="tag" href="/tag/paraphrased/page/1/">paraphrased</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“A woman is like a tea bag; you never know how strong it is until it's in hot water.”</span>
        <span>by <small class="author" itemprop="author">Eleanor Roosevelt</small>
        <a href="/author/Eleanor-Roosevelt">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="misattributed-eleanor-roosevelt"> 
            
            <a class="tag" href="/tag/misattributed-eleanor-roosevelt/page/1/">misattributed-eleanor-roosevelt</a>
            
        </div>
    </div>

    <div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“A day without sunshine is like, you know, night.”</span>
        <span>by <small class="author" itemprop="author">Steve Martin</small>
        <a href="/author/Steve-Martin">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="humor,obvious,simile"> 
            
            <a class="tag" href="/tag/humor/page/1/">humor</a>
            
            <a class="tag" href="/tag/obvious/page/1/">obvious</a>
            
            <a class="tag" href="/tag/simile/page/1/">simile</a>
            
        </div>
    </div>

    <nav>
        <ul class="pager">
            
            
            <li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">→</span></a>
            </li>
            
        </ul>
    </nav>
    </div>
    <div class="col-md-4 tags-box">
        
            <h2>Top Ten tags</h2>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 28px" href="/tag/love/">love</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 26px" href="/tag/inspirational/">inspirational</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 26px" href="/tag/life/">life</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 24px" href="/tag/humor/">humor</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 22px" href="/tag/books/">books</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 14px" href="/tag/reading/">reading</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 10px" href="/tag/friendship/">friendship</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 8px" href="/tag/friends/">friends</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 8px" href="/tag/truth/">truth</a>
            </span>
            
            <span class="tag-item">
            <a class="tag" style="font-size: 6px" href="/tag/simile/">simile</a>
            </span>
            
        
    </div>
</div>

    </div>
    <footer class="footer">
        <div class="container">
            <p class="text-muted">
                Quotes by: <a href="https://www.goodreads.com/quotes">GoodReads.com</a>
            </p>
            <p class="copyright">
                Made with <span class="zyte">❤</span> by <a class="zyte" href="https://www.zyte.com">Zyte</a>
            </p>
        </div>
    </footer>

</body></html>
"""

QUOTE_PAGE_HTML_2 = """
<html>
<body>
<div class="quote">
    <span class="text">"Second page quote"</span>
    <small class="author">Author2</small>
    <a href="/author/Author2">About</a>
</div>

<!-- NO next button = stops crawl -->
</body>
</html>
"""


LAST_PAGE_HTML = """
<html>
<body>

<div class="quote">
    <span class="text">"Final Quote"</span>
    <small class="author">Final Author</small>

    <div class="tags">
        <a class="tag">end</a>
    </div>

    <a href="/author/Final-Author">About</a>
</div>

</body>
</html>
"""


AUTHOR_PAGE_HTML = """
<html>
<body>

<h3 class="author-title">Author1</h3>
<div class="author-description">This is a bio.</div>

</body>
</html>
"""


# =========================================================
# TEST 1: crawlQuotes extracts quotes + authors + tags
# =========================================================

@patch("src.crawler.requests.get")
def test_crawl_quotes_basic(mock_get):

    mock_get.side_effect = [
        Mock(status_code=200, text=QUOTE_PAGE_HTML),
        Mock(status_code=200, text=LAST_PAGE_HTML)
    ]

    content, authors = crawlQuotes([], "https://quotes.toscrape.com")

    # basic structure checks
    assert isinstance(content, list)
    assert isinstance(authors, set)

    # should extract quotes
    assert any("The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking" in text for _, text in content)
    assert any("Final Quote" in text for _, text in content)

    # should extract author links
    assert any("/author/Albert-Einstein" in a for a in authors)
    assert any("/author/Final-Author" in a for a in authors)


# =========================================================
# TEST 2: pagination stops correctly
# =========================================================

@patch("src.crawler.requests.get")
def test_crawl_quotes_stops_at_last_page(mock_get):

    mock_get.return_value = Mock(status_code=200, text=LAST_PAGE_HTML)

    content, authors = crawlQuotes([], "https://quotes.toscrape.com")

    assert len(content) == 1
    assert len(authors) >= 1


# =========================================================
# TEST 3: crawlAuthors extracts name + bio
# =========================================================

@patch("src.crawler.requests.get")
def test_crawl_authors(mock_get):

    mock_get.return_value = Mock(status_code=200, text=AUTHOR_PAGE_HTML)

    authors = {"https://quotes.toscrape.com/author/Author1"}

    content = crawlAuthors([], authors)

    assert len(content) == 1

    url, text = content[0]

    assert "Author1" in text
    assert "This is a bio." in text


# =========================================================
# TEST 4: full pipeline (crawl → authors)
# =========================================================

@patch("src.crawler.requests.get")
def test_full_crawl(mock_get):

    def fake_get(url, *args, **kwargs):
        if "/page/2" in url:
            return Mock(status_code=200, text=QUOTE_PAGE_HTML_2)
        return Mock(status_code=200, text=QUOTE_PAGE_HTML)

    mock_get.side_effect = fake_get

    content = crawl()

    assert isinstance(content, list)
    assert len(content) >= 2

    texts = [t for _, t in content]

    assert any("The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking" in t for t in texts)
    assert any("Second page quote" in t for t in texts)


# =========================================================
# TEST 5: handles bad HTTP response safely
# =========================================================

@patch("src.crawler.requests.get")
def test_handles_bad_response(mock_get):

    mock_get.return_value = Mock(status_code=404, text="")

    content, authors = crawlQuotes([], "https://quotes.toscrape.com")

    assert content == []
    assert authors == set()
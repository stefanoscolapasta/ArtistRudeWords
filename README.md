# ArtistRudeWords <br/>
## ABOUT
**PYTHON SCRIPT** to count how many bad/swear words an artist said based on his songs lyrics featured on [genius.com](www.genius.com)<br/><br/> 

### USAGE

**Clone the repo** and launch the script from the folder by typing <br/>`python main.py` in command-line

* You can **choose** which artist to search
* To add a new artist you need to look for the [final part of their genius.com URL](www.genius.com)
    * **Example**: Say you want to add Lil Uzi Vert to the list of artists that can be searched
    * You need to look for their [genius.com](www.genius.com) URL -> [https://genius.com/artists/Lil-uzi-vert](https://genius.com/artists/Lil-uzi-vert)
    * Select the final '/', in our case only **'Lil-uzi-vert'**
    * Now **add it** to the list <br/>
    ![](assets/spiegazioneGitHub1.png)
    and so <br/>
    ![](assets/spiegazioneGitHub2.png)
    * You're done!
<br/><br/> 
* Now select the artist from the menu<br/>
  ![](assets/menu.png)

* And finally choose the artist's main language<br/>
  ![](assets/menuLanguage.png)
  
* It will automatically open the artist's Genius webpage and scroll through all the songs featured on the website<br/>
  ![](assets/scrolling.png)

* Once finished collecting all links to the songs it will close the webpage and start downloading all the lyrics<br/>
  ![](assets/analyze.png)
  
* If a link is corrupted the script will let you know it did not retrieve the lyrics of that song<br/>
  ![](assets/lyrics_fail.png)
  
* The final result will be a bar graph showing the use of swear/bad words during his career  <br/>
   > As seen, I have to fix the xticks spacing when the words are too many<br/>
![](assets/graph.png)

## <br/>TODO
- [ ] Improve the resulting graphs
- [ ] Try to use Requests and BeautifulSoup for link collection instead of Selenium Web-Driver to get a faster script
- [ ] Add multiple options
- [ ] Make the command-line menu more user-friendly
- [ ] Divide swear-words by type <br/> 
         1. Sex-oriented bad words<br/>
         2. Race-oriented insults<br/>
         3. General insults<br/>
         4. Etc.<br/>
- [ ] Add multiple languages

## Author

* [Stefano Scolari](https://www.linkedin.com/in/stefano-scolari-7a9440170/)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © <a href="http://fvcproductions.com" target="_blank">FVCproductions</a>.

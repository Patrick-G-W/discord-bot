<h2>This list will be extended as I create more commands for the bot.</h2>

<h3>Commands:</h3>
<b>.imdb "&#60movie or tv show title&#62"</b> - gets movie/tv title from IMDb and posts a link of it in the channel. Using double quotes is not necessary, but usually yields more accurate results.<br>
<b>.images &#60search term&#62</b> - searches google images using the supplied search term and returns the first result. Double quotes same as above.<br>
<b>.help</b> - displays commands that the bot can do<br>
<b>.dbremove "&#60username#discriminator&#62"</b> - removes user from the user database. This command should be used with the following formatting: .dbremove &#60name&#62#&#60number&#62 NOTE: the user will be re-added to the database if they are still in the server when the bot restarts.<br>
<b>.dbupdate</b> - updates the database with any new information that the users have. This includes name, avatar and roles.<br>
<b>.givepoints "&#60username#discriminator&#62" X</b> - gives the user X amount of points. <b>Can only be used by administrators.</b><br>
<b>.removepoints "&#60username#discriminator&#62" X</b> - removes X amount of points from the user. <b>Can only be used by administrators.</b><br>

<h3>FAQ:</h3>
<b>Q: I have changed the role of a user, but the database still shows the old roles. How can I fix this?</b><br>
A: Changing roles does not automatically update the database, only a user changing their avatar, username or discriminator. To update the database manually, run .dbupdate

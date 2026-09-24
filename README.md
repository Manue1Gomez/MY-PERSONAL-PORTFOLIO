# Manuel Gomez Portfolio (Flask)

## Pinakamadaling patakbuhin
- **Windows:** double-click `run.bat`
- **Mac/Linux:** `./run.sh`
- **VS Code:** buksan ang folder, buksan ang terminal at i-type:
  `pip install -r requirements.txt` tapos `python app.py`
  (o pindutin ang F5, ayos na ang `.vscode/launch.json`)

Awtomatikong magbubukas ang browser sa http://127.0.0.1:5000

## Ipapalit mo
- `static/resume.pdf` = ang resume mo (MANUEL-UPDATED-RESUME.pdf). Palitan lang ng file na may parehong pangalan kung mag-update.
- `static/photo.jpg` = palitan ng actual na larawan mo.
- `app.py` > `PROFILE["socials"]` = ilagay ang GitHub/LinkedIn links.

## Contact form
Naka-save ang messages sa `messages.txt`. Para ma-email sa iyo, i-set ang `SMTP_HOST`,
`SMTP_USER`, `SMTP_PASSWORD` (`SMTP_PORT` default 587). Sa Gmail, gumamit ng App Password.

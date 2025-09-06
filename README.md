# BetterPergamum  

**BetterPergamum** – A Reverse Engineering solution for interacting with the Pergamum library system in a more user-friendly and extensible way.  

## Overview  

The **Pergamum** system is widely used in Brazilian universities as a library management platform. However, its interface and accessibility can be limited for automation, research, or integration with modern applications.  

**BetterPergamum** was built as a **proof of concept in reverse engineering**:  
- By analyzing the HTTP requests, sessions, and cookies behind Pergamum’s web interface.  
- Reconstructing and exposing the hidden endpoints in a structured and programmable way.  
- Wrapping the original system with a **Streamlit-based prototype** for a more intuitive experience.  

This project demonstrates how reverse engineering can be applied in an educational context to better understand legacy systems and extend their usability.  

## Features  

- **Login simulation** – Automates session and cookie handling.  
- **Book search** – Queries titles directly via the reverse-engineered endpoints.  
- **Loan tracking** – Displays active loans and due dates.  
- **Modern interface** – Built with [Streamlit](https://streamlit.io/) for fast prototyping.  

## Tech Stack  

- **Python 3**  
- **Streamlit** (UI)  
- **Requests + BeautifulSoup (bs4)** – For handling HTTP traffic and parsing responses.  
- **Reverse Engineering tools** – Manual inspection, `curl`, `mitmproxy`, and browser DevTools.  

## Getting Started  

You can use the system by the [streamlit app url](https://betterpergamum.streamlit.app/) or cloning the repository and running it yourself.
I may upload all the notes I did in order to reverse engineer the entire API or upload an unofficial documentation, so you could see it and implement it for yourself.

## Disclaimer

This project was developed strictly for academic and educational purposes in the context of software reverse engineering.
It is not affiliated with or endorsed by the official Pergamum system.
Use responsibly and respect your institution’s policies regarding system usage.

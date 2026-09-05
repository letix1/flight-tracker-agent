# Flight Tracker Agent

A conversational agent that answers questions about live air traffic, using real-time aircraft position data from the OpenSky Network API. Ask it about a specific flight or a region, and it decides on its own when to fetch live data versus when it already knows enough to answer.


## Motivation

Most LLM-based chat tools can only talk about what's in their training data, which is fine for static facts but useless for anything that changes minute to minute, like where a plane actually is right now. This project pairs an LLM with a live data source through tool use, so the agent can ground its answers in real, current aircraft positions instead of guessing or refusing to answer.


## How it works

The agent is built on Claude's tool-use API. Two tools are defined:

- **`find_by_callsign`**: looks up a specific aircraft currently airborne by its flight callsign (e.g. `KLM1960`)
- **`find_in_bounding_box`**: finds all aircraft currently within a geographic bounding box (latitude/longitude range)

When you ask a question, Claude decides whether it needs live data to answer, and if so, which tool to call and with what parameters. For location-based questions (e.g. "near London," "over the Netherlands"), Claude estimates a reasonable bounding box on its own, it isn't given exact coordinates anywhere in the conversation.


## Data source

Live aircraft data comes from the [OpenSky Network](https://opensky-network.org/), a community-run ADS-B receiver network that provides free, real-time flight tracking data for research and non-commercial use. This project uses anonymous (unauthenticated) access, which has a lower rate limit than an authenticated account, but requires no account setup.


## Example

```
You: how many flights are over the netherlands right now

Agent: There are currently **74 flights** over the Netherlands right now.
The flights include a mix of commercial airlines, cargo carriers, and
private aircraft from various countries including the Netherlands
(KLM and other Dutch operators), Belgium, Germany, United Kingdom...
```


## Project structure

```
flight-tracker-agent/
  test_setup.py          checks the OpenSky API is reachable
  opensky_tools.py       functions that query OpenSky (by callsign, by bounding box)
  agent.py               the Claude tool-use agent and conversation loop
  requirements.txt
  README.md
```

## Limitations

- **No schedule or delay data.** OpenSky provides live position data (altitude, speed, heading, location), not scheduled departure/arrival times, so questions like "is this flight delayed" can't be answered with this data source. The agent is scoped to live tracking questions only.
- **Anonymous rate limits.** Without an authenticated OpenSky account, requests are limited to roughly once every 10 seconds. Rapid back-to-back questions in a single session could occasionally hit this limit.
- **Bounding boxes for named places are estimates.** Claude picks reasonable latitude/longitude bounds for a place mentioned in a question (e.g. "near London"), but these aren't precise or verified against an actual geocoding service, so results for less well-known places may be less reliable.
- **No conversation memory beyond the current session.** Each run starts fresh; there's no persistence of past queries or results between sessions.


## Author

Letizia Bianchi ([LinkedIn](https://linkedin.com/in/letizia-ida-bianchi))
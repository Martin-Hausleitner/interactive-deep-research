### The Single Best Pick: The Self-Build Hybrid Stack (Matrix Synapse + Mautrix Bridges + GoLogin + Claude Computer Use)

**Why this is the winner:** 
No commercial tool on the market natively supports a unified, proactive cold-outreach sequence across Instagram, WhatsApp, X/Twitter, and LinkedIn without requiring official API access. Commercial platforms either strictly limit your channels (e.g., HeyReach is LinkedIn-only [1, 2], La Growth Machine lacks WhatsApp and Instagram [3, 4]), or they rely on highly detectable Chrome extensions that inject code into the DOM, which platforms quickly flag to ban your burner accounts [5, 6]. 

By building a custom stack, you solve the three biggest bottlenecks of burner-account automation:
1. **Unrestricted Omnichannel Routing:** Using open-source Mautrix bridges, you can link unofficial APIs for Instagram, WhatsApp, and X/Twitter directly into a single Matrix homeserver, giving you the "Unified Inbox" experience without paying enterprise commercial fees [7-9].
2. **Total Infrastructure Isolation:** By running each burner account inside a dedicated **GoLogin** profile tied to a residential proxy, you spoof the browser fingerprint and IP address, bypassing "impossible travel" and datacenter IP bans [10, 11].
3. **Undetectable Execution:** Standard headless browsers (Puppeteer/Playwright) are instantly detected by platforms like LinkedIn and Instagram [12, 13]. By using **Claude Computer Use**, the AI interacts with your GoLogin browser visually—reading the screen and moving the mouse just like a human. Because it bypasses the DOM entirely and operates at human speeds (10-30 seconds per action), it completely evades bot detection [14-16].

---

### Step-by-Step Setup Plan

**1. Infrastructure & Isolation Setup**
Rent a VPS and purchase dedicated residential proxies (data-center IPs will trigger instant bans) [11, 17]. Install the **GoLogin** antidetect browser and create a strictly isolated profile for each burner account, assigning a unique proxy and spoofed device fingerprint to each [10, 18].

**2. Account Warm-Up Protocol**
Do not deploy automation immediately. Log into your burner accounts via GoLogin and manually execute a 3-to-4-week warm-up phase [19]. For LinkedIn, view profiles, like posts, and send 2-3 connection requests per day in week 2, scaling to 15-20 a day by week 4 [20-22]. For WhatsApp, chat strictly with saved contacts for the first 7 days before slowly messaging 5-10 strangers per day [23].

**3. Deploy the Matrix Hub**
Install a **Matrix Synapse** homeserver via Docker [24, 25]. Deploy the necessary open-source Mautrix bridges to your server, specifically `mautrix-meta` (for Instagram DMs), `mautrix-whatsapp`, and `mautrix-twitter` [9]. 

**4. Bridge Authentication**
Connect your warmed-up burner accounts to the bridges. Start a chat with the respective bridge bots on your Matrix client (e.g., `@whatsappbot:yourdomain`). Send the `login` command and authenticate (e.g., by scanning the WhatsApp QR code or entering Instagram credentials) [26, 27]. All your multi-channel DMs will now aggregate into your Matrix client [7].

**5. Configure Claude Computer Use (The Execution Engine)**
Set up an Anthropic API environment utilizing the Claude Computer Use reference implementation [28]. Instruct Claude to take over the GoLogin browser profiles to execute your cross-channel sequences visually. For example, prompt the AI to: *"Read this prospect list. Open the LinkedIn tab, search the name, and click connect. Log the result. If no acceptance after 3 days, open the Instagram tab, search their handle, and type this DM."* [15, 29, 30]

**6. Throttle Volume and Manage Replies**
Enforce strict rate limits to prevent behavioral bans. Cap your Claude-driven automated proactive outreach to 15-20 connection requests/day on LinkedIn [31], 30-50 proactive messages/day on WhatsApp [32, 33], and 20-30 DMs/day on Instagram [34]. When prospects reply, use your centralized Matrix inbox to take over the conversation manually and close the lead [8].
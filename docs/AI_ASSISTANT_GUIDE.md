# How Ask Bridge AI Works (Easy English)

## What it can do

The assistant reads **real source records in the project catalog** and the result of the
current saved payment plan. Its main jobs are:

1. **Tuition fees:** Show published program examples and clickable university sources.
2. **Living costs and visa funds:** Explain public benchmarks and clearly separate visa
   requirements from living expenses. Historical values are labeled.
3. **Exchange rates:** Fetch a published *reference* rate when the public FX service
   is available. It is not a bank quote and has no bank fees.
4. **Credit tips:** Show simple official guidance for each supported country.
5. **Payment planning:** Explain entered bank quotes, deadline suitability, reserve
   checks, possible costs and rejected options. No real payment is made.

## Questions to try

- What can you do?
- Tuition fees in the UK
- Living costs in Japan
- What are the UK visa financial requirements?
- What is the exchange rate GBP to JPY?
- How can I build credit in Australia?
- How do I compare transfers from China to Australia?
- Why was my payment route rejected? (after creating a plan)
- What happens if the exchange rate rises 5%? (build plan first, then use Budget simulator)

The AI panel offers buttons to go to the next useful page and links to the available sources.
If a value or eligible transfer route is missing, the assistant says it is missing.

## What it cannot do

- Verify a user-provided bank transfer quote by itself.
- Guarantee delivery, choose a legally eligible route, or transfer actual money.
- Check your real credit score, identify a genuine invoice with certainty, or
  predict future exchange rates.
- Offer full general-purpose real-time financial research beyond the catalog/APIs.

### Optional Gemini

If `GEMINI_API_KEY` is set on the server, Gemini can provide **optional rewording**
for the already-calculated explanation. The deterministic financial answer and original
sources remain separate and authoritative. If the key is absent or provider unavailable,
normal data-backed answers continue to work.

### Security

No API credentials are sent to the web browser. StudentBridge requires explicit approval
for test-only transactions; test events are stored in MySQL with an HMAC audit chain.
This demo does not include independent user authentication or production banking features.

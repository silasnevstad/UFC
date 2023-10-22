# Universal Fact-Checker (UFC)

## What is UFC?
UFC is a tool designed to help you check the credibility and factualness of any claim, it does this by providing soures either supporting or opposing the claim. It leverages GPT and uses a variety of reputable sources to determine the validity of a claim.

## How does it work?
UFC operates in a structured, step-wise manner to dissect, verify, and substantiate claims, ensuring each step is backed by credible sources. Here's an overview of its operation:

### Claim Segmentation
  - Input: A body of text containing one or more claims.
  - Operation: The text is analyzed and broken down into individual claims for verification.
### Claim Verification
  - Input: Individual claims.
  - Operation: Each claim is processed to determine its topic and search terms.
### Source Retrieval
  - Input: Claims and corresponding topics/search terms.
  - Operation: Executes queries through APIs and web scrapers to retrieve reputable information pertinent to each claim.
### Claim Verification
  - Input: Claims and gathered reputable information.
  - Operation: Analyzes the retrieved information to substantiate or refute each claim, gathering a collection of supporting or contradicting evidence. Compiles the results into a structured output.
  - Output: A detailed report listing each claim, its substantiation status and references to the supporting/opposing sources.

## Sources

### APIs
- [Wikipedia API](https://pypi.org/project/wikipedia/)
- [Europeana]()
- [DPLA]()

### Sites
- [National Archives](https://www.archives.gov/)
- [Library of Congress](https://www.loc.gov/)
- [Smithsonian](https://www.si.edu/)
- [National Geographic](https://www.nationalgeographic.com/)
- [History Net](https://www.historynet.com/)


## Future Enhancements
- Expand the domain coverage beyond history to include science, current events, and other relevant domains.
- Implement feedback loop to allow users to provide feedback on the accuracy of the substantiation reports.
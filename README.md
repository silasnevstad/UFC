# Verifi

## What is Verifi?
Verifi is a tool designed to help you check the credibility and factualness of any claim, it does this by providing soures either supporting or opposing the claim. It leverages GPT and uses a variety of reputable sources to determine the validity of a claim.

## How does it work?
UFC operates in a structured, step-wise manner to dissect, verify, and substantiate claims, ensuring each step is backed by credible sources. Here's an overview of its operation:

### Claim Segmentation
  - Input: A body of text containing one or more claims.
  - Operation: The text is analyzed and broken down into individual claims for verification.
### Claim Identification
  - Input: Individual claims.
  - Operation: Each claim is processed to determine its genre and suggested search terms.
### Source Retrieval
  - Input: Claims and corresponding topics/search terms.
  - Operation: Retrieves data through APIs and web scrapers to gain reputable information pertinent to each claim.
### Claim Verification
  - Input: Claims and gathered reputable information.
  - Operation: Analyzes the retrieved information to substantiate or refute each claim, gathering a collection of supporting or contradicting evidence. Compiles the results into a structured output.
  - Output: A detailed report listing each claim, its substantiation status and references to the supporting/opposing sources.


## Future Enhancements
- Expand the domain coverage to include other relevant domains.
- Implement feedback loop to allow users to provide feedback on the accuracy of the substantiation reports.

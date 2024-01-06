# Building_LLM_Applications

## Data Preparation Flow for Retrieval Augmented Generation(RAG)

![image](https://github.com/vsingh9076/Building_LLM_Applications/assets/46970126/658560eb-db1c-4e73-ae9f-3c925e3d8ad6)

### Why Chunk?

In the realm of applications, the game-changer lies in how you mold your data - be it markdown, PDFs, or other textual files. Picture this: you've got a hefty PDF, and you're eager to fire questions about its content. The catch? Traditional methods of tossing the entire document and your question at the model fall flat. Why? Well, let's talk about the limitations of the model's context window.

Picture the context window as a peek into the document, often limited to just a page or a few. Now, sharing your entire document at once? Not so realistic. But fear not!

The magic trick lies in chunking your data. Break it down into digestible portions, sending only the most relevant chunks to the model. 
This way, you're not overwhelming it, and you get the precise insights you crave.

By breaking down our structured documents into manageable chunks, we empower our LLM to process information with unparalleled efficiency. 
No longer limited by page constraints, this approach ensures that crucial details aren't lost in the shuffle.

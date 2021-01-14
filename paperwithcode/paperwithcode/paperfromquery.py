from paperswithcode import PapersWithCodeClient


def papers_from_query(query):
    """
    docstring
    """
    client = PapersWithCodeClient()
    papers = client.paper_list(q=query)
    results = []
    for paper in papers.results:
        repository = client.paper_repository_list(paper_id=paper.id)
        if len(repository) > 0:
            repository = repository[0]
        else:
            repository = None
        if paper.conference is not None:
            conference = client.conference.get(conference_id=paper.conference)
        else:
            conference = None
        paper_detail = {
            "title": paper.title,
            "authors": ", ".join(paper.authors),
            "abstract": paper.abstract,
            "publicationOrg":
            conference.name if conference is not None else "",
            "year": paper.published.year,
            "pdfUrl": paper.url_pdf,
            "publicationUrl": paper.conference_url_pdf,
            "codeUrl": repository.url if repository is not None else "",
        }
        results.append(paper_detail)
    return results

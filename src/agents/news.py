from typing import Optional
from llm.chat import get_response_from_llm
from config import ModelName


def extract_summary(text: str) -> Optional[str]:
    prompt = f"""
    Extract the key points from this article and summarize it in one sentence:\n
    {text}
    """
    result = get_response_from_llm(prompt)
    return result


if __name__ == "__main__":
    text = """World-first experimental cancer treatment paves way for clinical trial  
28 February 2025

An experimental treatment for an aggressive and lethal brain cancer has today been published in Nature Medicine, paving the way for a clinical trial to be conducted by researchers at The Brain Cancer Centre.   

 The peer-reviewed paper details experimental treatment for glioblastoma developed by Professor Georgina Long AO, University of Sydney medical oncologist and Medical Director of the Melanoma Institute Australia. 

At a glance
Publication of experimental treatment for glioblastoma paves the way for a clinical trial to be conducted by researchers at The Brain Cancer Centre.
The international clinical trial will scientifically investigate the efficacy of the experimental approach within a large cohort of eligible glioblastoma patients.
The Brain Cancer Centre was founded by Carrie’s Beanies 4 Brain Cancer and established in partnership with WEHI, with support from the Victorian Government.  
Glioblastoma is a highly aggressive and lethal brain cancer with an average survival time of 12 to 18 months. Only 25% of patients survive more than one year and less than 5% survive more than 3 years.

The new publication shares the experimental treatment given to a patient diagnosed with glioblastoma.

Prof Long used her expertise in immunotherapy and drew on melanoma science to devise, lead and administer the treatment.

It is the first documented use of neoadjuvant triple immunotherapy in glioblastoma, involving a combination of three checkpoint inhibitor immunotherapies (drugs that activate the immune system, instructing T-cells to kill tumour cells) administered prior to surgery.

The paper details that, when surgically removed, the tumour treated with immunotherapy showed increased diversity, abundance and activation of immune cells, compared to the tumour prior to receiving immunotherapy.

These immune cells may recognise and attack cancer cells: their increased presence may suggest a strong immune response. At the time of final submission of the journal paper, the patient had no clear signs of cancer recurrence after more than 18 months.

“My hypothesis was that we could administer combination immunotherapy as first line treatment before surgery to boost the immune system and activate T-cells to target the brain tumour – an approach I had previously developed successfully in both stage 3 melanoma and melanoma that had spread to the brain,” said lead author, Prof Long.

“This has never been done before and what this trial will do is establish whether this approach is feasible or effective for the treatment of glioblastoma.”

Testing treatment hypothesis
An Australian-led international clinical trial will scientifically investigate the efficacy of the approach within a large cohort of eligible glioblastoma patients and could commence within a year.

The study will trial the use of double immunotherapy. In some patients, double immunotherapy will be combined with chemotherapy.

The trial will be led by The Brain Cancer Centre, which has world-leading expertise in glioblastoma.

“I am delighted to be handing the baton to Dr Jim Whittle, a leading Australian neuro-oncologist at Peter MacCallum Cancer Centre, The Royal Melbourne Hospital and Co-Head of Research Strategy at The Brain Cancer Centre, to commence a broader scientific study to scientifically determine if – and how – this process might work in treating glioblastoma,” said Prof Long, who also secured drug access for the clinical trial.

“While we are buoyed by the results of this experimental treatment so far, a clinical trial in a large group of patients would need to happen before anyone could consider it a possible breakthrough.”

Dr Whittle, also a laboratory head at WEHI, said: “We are pleased to be able to build on this exciting work by diving into the process of designing a clinical trial, which takes time, care and accuracy.

“When that process is complete, the result will be a world first clinical trial that enables us to thoroughly test the hypothesis against a representative sample of patients.”

The Brain Cancer Centre was founded by Carrie’s Beanies 4 Brain Cancer and established in partnership with WEHI with support from the Victorian Government.

The centre brings together a growing network of world-leading oncologists, immunologists, neurosurgeons, bioinformaticians and cancer biologists.

Commencement of recruitment for the clinical trial will be announced by The Brain Cancer Centre at a later date and will be limited to eligible patients.
   """
    summary = extract_summary(text)
    print(summary)

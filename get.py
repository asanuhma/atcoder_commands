import os
from urllib import request
from bs4 import BeautifulSoup

def get_samples(url: str, dst: str):
    """
    get sample cases from url of ABC
    ----------
    input
    url: url of ABC (ex: "https://atcoder.jp/contests/abc173/tasks/abc173_a")
    dst: path of project folder
    ----------
    result
    dst
    |- in
    |  |- 1.txt
    |  |  ...
    |  -- n.txt
    |
    -- out
       |- 1.txt
       |  ...
       -- n.txt
    """
    html = request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("section")

    sample_names = ["Sample Input", "Sample Output"]
    sample_in_out = [[t for t in tags if name in t.find("h3").string] for name in sample_names]
    titles = [set([s.find("h3").string.split()[-1] for s in samples]) for samples in sample_in_out]
    assert titles[0] == titles[1], "Fail to scrape samples"

    folders = [os.path.join(dst, folder) for folder in ["in", "out"]]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for folder, samples in zip(folders, sample_in_out):
        for sample in samples:
            with open(os.path.join(folder, sample.find("h3").string.split()[-1])+".txt", 'w') as f:
                f.write(sample.find("pre").string)
    files = [set(os.listdir(folder)) for folder in folders]
    assert files[0] == files[1], "Fail to save samples"
    print(f"Complete saving {len(files[0])} samples!")

if __name__ == "__main__":
    print("URL:", end=" ")
    url = input()
    print("Path of project folder:", end=" ")
    dst = input()
    get_samples(url, dst)

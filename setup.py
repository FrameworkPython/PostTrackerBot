from setuptools import setup, find_packages

setup(
    name="post_tracker",
    version="0.3.2",
    description="A package to track Iranian post packages",
    author="FrameworkPython",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        "bs4>=0.0.2",
        "httpx>=0.27.0,<0.28",
        "pydantic>=1.10.12",
        "rich>=13.8.0",
        "user-agent>=0.1.10"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
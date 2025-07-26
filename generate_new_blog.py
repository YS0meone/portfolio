from datetime import datetime, date
from pathlib import Path
from ruamel.yaml import YAML
import argparse
from datetime import datetime


BLOG_TEMPLATE = """# {date} - Daily Drill

## 🎯 Daily Goals

- [x] Review Anki Deck
- [x] Lumosity training
- [x] Leetcode
- [x] Developing laplace
- [x] Langchain Learning

## 📝 What I learned:

### Leetcode Problem

#### Thinking Process

#### Complexity Analysis

**Time Complexity: O()**
**Space Complexity: O()**

#### Key Takeaways

## 🚀 Resources that Requires Further Study


## 📃 Summary and Reflection
"""


def create_new_markdown(new_date: date) -> None:
    base_root = Path() / "docs" / "learn"
    year_folder = new_date.strftime("%Y")
    month_folder = new_date.strftime("%m-%B").lower()
    file_name = new_date.strftime("%Y-%m-%d") + ".md"
    blog_date = new_date.strftime("%B %d, %Y")

    new_md_path = base_root / year_folder / month_folder / file_name
    if not new_md_path.parent.exists():
        print(f"Creating new folders for {new_md_path}")
        new_md_path.parent.mkdir(parents=True)

    if new_md_path.exists():
        print(f"Markdown file already exists, skipping creation")
        return

    new_md_path.touch()
    new_md_path.write_text(BLOG_TEMPLATE.format(
        date=blog_date), encoding="utf-8")
    print(f"✅ Created new blog post: {new_md_path}")


def insert_index(new_date: date) -> None:
    blog_month_section = new_date.strftime("%B, %Y")
    year_folder = new_date.strftime("%Y")
    month_folder = new_date.strftime("%m-%B").lower()
    file_name = new_date.strftime("%Y-%m-%d") + ".md"

    config_yaml = Path("mkdocs.yml")
    if not config_yaml.exists():
        print("Error: config file does not exist, abort.")
        return

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096

    # Fix: Add encoding when reading
    with open(config_yaml, "r", encoding='utf-8') as config:
        data = yaml.load(config)

    nav = data.get('nav', [])
    new_file = f"learn/{year_folder}/{month_folder}/{file_name}"

    # Navigate through the structure correctly
    for section in nav:
        if isinstance(section, dict) and 'Learn' in section:
            learn_section = section['Learn']
            for item in learn_section:
                if isinstance(item, dict) and 'Daily Logs' in item:
                    daily_logs = item['Daily Logs']

                    # Find or create the month section
                    month_section_found = False
                    for month_item in daily_logs:
                        if isinstance(month_item, dict) and blog_month_section in month_item:
                            month_logs = month_item[blog_month_section]
                            month_section_found = True

                            if new_file not in month_logs:
                                month_logs.append(new_file)

                                # Write back to file
                                with open(config_yaml, "w", encoding='utf-8') as config_file:
                                    yaml.dump(data, config_file)
                                print(f"✅ Added {new_file} to navigation")
                            else:
                                print(f"📝 {new_file} already in navigation")
                            return

                    # If month section doesn't exist, create it
                    if not month_section_found:
                        new_month_section = {blog_month_section: [new_file]}
                        daily_logs.append(new_month_section)

                        # Write back to file
                        with open(config_yaml, "w", encoding='utf-8') as config_file:
                            yaml.dump(data, config_file)
                        print(
                            f"✅ Created new month section and added {new_file} to navigation")
                    return

    print("❌ Could not find navigation structure to update")


def main():
    
    parser = argparse.ArgumentParser(description='Generate a new blog post.')
    parser.add_argument('-d', '--date', type=str, 
                        help='Custom date in YYYY-MM-DD format. Defaults to today.')
    args = parser.parse_args()
    
    if args.date:
        try:
            new_date = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print("Error: Date format should be YYYY-MM-DD")
            return
    else:
        new_date = date.today()
    
    print(f"Creating blog post for: {new_date}")
    create_new_markdown(new_date)
    insert_index(new_date)


if __name__ == '__main__':
    main()

"""
Unit tests for README.md content changes.

This repository is a GitHub profile README (no application source code),
so these tests validate the structure and content of README.md itself:
required sections, badges, links, and markup balance introduced by this PR.
"""

import re
import unittest
from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent / "README.md"


class ReadmeTestCase(unittest.TestCase):
    """Base test case that loads README.md once for all tests."""

    @classmethod
    def setUpClass(cls):
        """
        Load the README content and its individual lines for the test class.
        
        Parameters:
        	cls (type): The test class receiving the shared README data.
        """
        cls.content = README_PATH.read_text(encoding="utf-8")
        cls.lines = cls.content.splitlines()


class TestReadmeExists(ReadmeTestCase):
    def test_readme_file_exists(self):
        self.assertTrue(README_PATH.is_file(), "README.md must exist at repo root")

    def test_readme_is_not_empty(self):
        """Verify that the README contains non-whitespace content."""
        self.assertGreater(len(self.content.strip()), 0)


class TestProfileViewsAndStatsSection(ReadmeTestCase):
    """Covers the renamed 'PROFILE VIEWS & STATS' block and its new badges."""

    def test_comment_marker_renamed(self):
        self.assertIn("<!-- PROFILE VIEWS & STATS -->", self.content)

    def test_old_comment_marker_removed(self):
        # The old marker "<!-- PROFILE VIEWS -->" (without "& STATS") must not
        # remain as an exact standalone line.
        self.assertNotIn("<!-- PROFILE VIEWS -->", self.lines)

    def test_profile_views_badge_present(self):
        self.assertIn(
            'src="https://komarev.com/ghpvc/?username=nicodolas', self.content
        )

    def test_followers_badge_present(self):
        """Verify that the README contains the GitHub followers badge with its expected alternative text."""
        self.assertIn(
            "https://img.shields.io/github/followers/nicodolas", self.content
        )
        self.assertIn('alt="GitHub Followers"', self.content)

    def test_total_stars_badge_present(self):
        self.assertIn("https://img.shields.io/github/stars/nicodolas", self.content)
        self.assertIn('alt="Total Stars"', self.content)

    def test_followers_and_stars_badges_are_separated_by_nbsp(self):
        pattern = re.compile(
            r'Profile Views" />\s*&nbsp;\s*<img src="https://img\.shields\.io/github/followers/nicodolas[^>]*/>\s*&nbsp;\s*<img src="https://img\.shields\.io/github/stars/nicodolas',
            re.MULTILINE,
        )
        self.assertRegex(self.content, pattern)


class TestGithubStatsMetricsHeading(ReadmeTestCase):
    def test_new_heading_present(self):
        self.assertIn("## GitHub Stats & Metrics", self.lines)

    def test_old_heading_absent(self):
        # The heading must have been renamed, not duplicated.
        self.assertNotIn("## GitHub Stats", self.lines)

    def test_heading_appears_exactly_once(self):
        """Verify that the GitHub Stats & Metrics heading appears exactly once."""
        count = sum(1 for line in self.lines if line == "## GitHub Stats & Metrics")
        self.assertEqual(count, 1)


class TestCodingActivitySection(ReadmeTestCase):
    def test_section_heading_present(self):
        self.assertIn("## Coding Activity & Contributions", self.lines)

    def test_wakatime_badge_and_link(self):
        self.assertIn(
            "[![wakatime stats](https://wakatime.com/badge/user/nicodolas.svg"
            "?style=for-the-badge)](https://wakatime.com/@nicodolas)",
            self.content,
        )

    def test_profile_summary_card_present(self):
        self.assertIn(
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            "profile-details?username=nicodolas",
            self.content,
        )

    def test_most_commit_language_card_present(self):
        self.assertIn(
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            "most-commit-language?username=nicodolas",
            self.content,
        )

    def test_repos_per_language_card_present(self):
        self.assertIn(
            "https://github-profile-summary-cards.vercel.app/api/cards/"
            "repos-per-language?username=nicodolas",
            self.content,
        )

    def test_contribution_snake_present(self):
        self.assertIn(
            "https://github-readme-contribution-grid-snake.vercel.app/snake.svg"
            "?username=nicodolas",
            self.content,
        )

    def test_section_contains_expected_number_of_images(self):
        # profile-details, most-commit-language, repos-per-language, snake = 4 <img> tags
        section_match = re.search(
            r"## Coding Activity & Contributions(.*?)</div>", self.content, re.DOTALL
        )
        self.assertIsNotNone(section_match, "Coding Activity section not found")
        img_count = len(re.findall(r"<img\s", section_match.group(1)))
        self.assertEqual(img_count, 4)


class TestDeveloperBadgesSection(ReadmeTestCase):
    def test_section_heading_present(self):
        self.assertIn("## Developer Badges & Recognition", self.lines)

    def test_language_badges_present(self):
        for lang in ("JavaScript", "TypeScript", "Python"):
            with self.subTest(lang=lang):
                self.assertIn(f"Code-{lang}-informational", self.content)

    def test_framework_badges_present(self):
        for framework in ("React", "Next.js"):
            with self.subTest(framework=framework):
                self.assertIn(f"Framework-{framework}-informational", self.content)

    def test_database_badge_present(self):
        self.assertIn("Database-PostgreSQL-informational", self.content)

    def test_tool_badges_present(self):
        for tool in ("Git", "Docker"):
            with self.subTest(tool=tool):
                self.assertIn(f"Tools-{tool}-informational", self.content)

    def test_editor_and_ide_badges_present(self):
        self.assertIn("Editor-NeoVim-informational", self.content)
        self.assertIn("IDE-VS_Code-informational", self.content)


class TestRandomInspirationHeading(ReadmeTestCase):
    def test_new_heading_present(self):
        self.assertIn("## Random Inspiration", self.lines)

    def test_old_heading_absent(self):
        self.assertNotIn("## Random Quote", self.lines)


class TestLetsConnectSection(ReadmeTestCase):
    def test_section_heading_present(self):
        self.assertIn("## Let's Connect", self.lines)

    def test_email_link_present(self):
        self.assertIn('<a href="mailto:nvanhieuk13@gmail.com">', self.content)

    def test_portfolio_link_present(self):
        self.assertIn('<a href="https://www.nekovibecoder.site/">', self.content)

    def test_github_link_present(self):
        self.assertIn('<a href="https://github.com/nicodolas">', self.content)

    def test_lets_connect_appears_once(self):
        count = self.content.count("## Let's Connect")
        self.assertEqual(count, 1)


class TestThirdPartyStatsFooterBadges(ReadmeTestCase):
    def test_comment_marker_present(self):
        self.assertIn("<!-- STATS FROM THIRD-PARTY SERVICES -->", self.content)

    def test_profile_views_tracked_badge(self):
        self.assertIn("Profile_Views-Tracked-B5EAD7", self.content)

    def test_last_updated_badge(self):
        self.assertIn("Last_Updated-2024-E9C5E9", self.content)

    def test_auto_updated_badge(self):
        self.assertIn("Auto_Updated_By-GitHub_Actions-C8A2C8", self.content)


class TestFooterAutomationNote(ReadmeTestCase):
    def test_automation_note_present(self):
        self.assertIn(
            "*This profile is automatically updated daily via GitHub Actions* ⚙️",
            self.content,
        )

    def test_thanks_for_visiting_message_retained(self):
        self.assertIn(
            "💚 **Thanks for visiting!** If you find value in my work, "
            "consider giving a ⭐ to my repos!",
            self.content,
        )


class TestMarkupStructureIntegrity(ReadmeTestCase):
    """Structural sanity checks that apply across the whole modified document."""

    def test_div_center_tags_are_balanced(self):
        """Verify that centered div elements are present and properly closed."""
        open_count = len(re.findall(r'<div align="center">', self.content))
        close_count = len(re.findall(r"</div>", self.content))
        self.assertGreater(open_count, 0)
        self.assertEqual(open_count, close_count)

    def test_all_img_tags_have_alt_attribute(self):
        img_tags = re.findall(r"<img\b[^>]*>", self.content)
        self.assertGreater(len(img_tags), 0)
        missing_alt = [tag for tag in img_tags if "alt=" not in tag]
        self.assertEqual(
            missing_alt, [], f"Found <img> tags missing alt attribute: {missing_alt}"
        )

    def test_all_anchor_tags_have_href(self):
        anchor_tags = re.findall(r"<a\b[^>]*>", self.content)
        self.assertGreater(len(anchor_tags), 0)
        missing_href = [tag for tag in anchor_tags if "href=" not in tag]
        self.assertEqual(
            missing_href,
            [],
            f"Found <a> tags missing href attribute: {missing_href}",
        )

    def test_no_unresolved_merge_markers(self):
        """Verify that the README contains no unresolved merge-conflict markers."""
        for marker in ("<<<<<<<", "=======", ">>>>>>>"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.content)

    def test_expected_section_headings_all_present(self):
        """Verify that the README contains all required section headings."""
        expected_headings = [
            "## About Me",
            "## Tech Stack",
            "## GitHub Stats & Metrics",
            "## Coding Activity & Contributions",
            "## Developer Badges & Recognition",
            "## Recent Activity",
            "## Random Inspiration",
            "## Let's Connect",
        ]
        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.lines)

    def test_section_headings_appear_in_expected_order(self):
        expected_order = [
            "## About Me",
            "## Tech Stack",
            "## GitHub Stats & Metrics",
            "## Coding Activity & Contributions",
            "## Developer Badges & Recognition",
            "## Recent Activity",
            "## Random Inspiration",
            "## Let's Connect",
        ]
        positions = [self.content.index(h) for h in expected_order]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
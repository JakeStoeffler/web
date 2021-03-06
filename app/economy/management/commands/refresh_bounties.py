'''
    Copyright (C) 2017 Gitcoin Core

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
from django.core.management.base import BaseCommand

from dashboard.models import Bounty


class Command(BaseCommand):
    """Define the management command to refresh bounties."""

    help = 'refreshes the triggers associated with current bounties'

    def add_arguments(self, parser):
        """Add argument handling to the refresh command."""
        parser.add_argument(
            '-r', '--remote',
            action='store_true',
            dest='remote',
            default=False,
            help='Pulls remote info about bounty too'
        )

    def handle(self, *args, **options):
        """Refresh all bounties.

        Attributes:
            all_bounties (QuerySet of Bounty): The queryset of all Bounties.
            fetch_remote (bool): Whether or not to fetch remote bounties.
                Defaults to: `False` unless user passes the remote option.

        """
        all_bounties = Bounty.objects.all()
        fetch_remote = options['remote']
        for bounty in all_bounties:

            if bounty.current_bounty:

                #stopgap to make sure that older versions of this bounty
                # are marked as current_bounty=False
                old_bounties = Bounty.objects.filter(
                    github_url=bounty.github_url,
                    title=bounty.title,
                    current_bounty=True,
                    pk__lt=bounty.pk,
                ).exclude(pk=bounty.pk).order_by('-created_on')
                for old_bounty in old_bounties:
                    old_bounty.current_bounty = False
                    old_bounty.save()
                    print("stopgap fixed old_bounty {}".format(old_bounty.pk))

                if fetch_remote:
                    bounty.fetch_issue_item()
                    bounty.fetch_issue_comments()
                    print('1/ refreshed {}'.format(bounty.pk))

            if not bounty.avatar_url:
                bounty.avatar_url = bounty.get_avatar_url()
                print('2/ refreshed {}'.format(bounty.pk))
            bounty.save()

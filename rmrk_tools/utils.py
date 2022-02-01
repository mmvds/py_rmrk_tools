import os


class Files:
    @staticmethod
    def get_local_media(filepath: str, filetype: str = 'all'):
        """
        Gather all files to pin to IPFS, ignoring any file prefixed with 'logo'
        :param filepath:
        :param filetype:
        :return: filepath of each file is returned in a list that can be iterated through to pinning
        """
        local_assets = []
        try:
            for path in os.listdir(filepath):
                asset_path = os.path.join(filepath, path)

                # skip collection logo
                if 'logo' in asset_path:
                    continue

                if path.endswith(filetype):
                    local_assets.append(asset_path)
                elif filetype == 'all':
                    local_assets.append(asset_path)
                else:
                    continue

            return local_assets
        except OSError:
            raise Exception('Check the path provided is correct')
